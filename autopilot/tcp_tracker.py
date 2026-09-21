#!/usr/bin/env python3
"""
TCP Work-Time Tracker — Track session start/end, task duration, idle detection,
automatic 30-min checkpoints, and daily summaries. Persists to JSONL.

Stores records alongside session.db in:
    <workspace>/tcp_tracker/

Records are JSONL (one JSON object per line) for append-only durability.
A daily summary is emitted as a separate record type.
"""

from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

WORKSPACE = Path(os.environ.get("TCP_WORKSPACE",
                                Path(__file__).resolve().parents[1]))

SESSION_DB_CANDIDATES = [
    WORKSPACE / "session.db",
    WORKSPACE / "data" / "session.db",
]

# Default storage directory — alongside session.db if found, else WORKSPACE
def _default_storage_dir() -> Path:
    for cand in SESSION_DB_CANDIDATES:
        if cand.exists():
            return cand.parent
    return WORKSPACE

STORAGE_DIR = Path(os.environ.get("TCP_STORAGE_DIR", _default_storage_dir())) / "tcp_tracker"
CHECKPOINT_INTERVAL_S = 30 * 60  # 30 minutes
IDLE_THRESHOLD_S = 5 * 60  # 5 minutes with no activity


class RecordType(str, Enum):
    SESSION_START = "session_start"
    SESSION_END = "session_end"
    TASK_START = "task_start"
    TASK_END = "task_end"
    CHECKPOINT = "checkpoint"
    IDLE_START = "idle_start"
    IDLE_END = "idle_end"
    DAILY_SUMMARY = "daily_summary"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _atomic_append(path: Path, record: dict[str, Any]) -> None:
    """Append a JSON record atomically using write+rename pattern."""
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False, default=str) + "\n"
    # Append mode is atomic on POSIX for lines < PIPE_BUF (4096 bytes)
    with open(path, "a", encoding="utf-8") as f:
        f.write(line)
        f.flush()
        os.fsync(f.fileno())


def _daily_log_path(day: Optional[str] = None) -> Path:
    day = day or _today_str()
    return STORAGE_DIR / f"tcp_{day}.jsonl"


# ---------------------------------------------------------------------------
# Data records
# ---------------------------------------------------------------------------

@dataclass
class Record:
    record_id: str = field(default_factory=lambda: uuid.uuid4().hex[:16])
    timestamp: str = field(default_factory=_now_iso)
    type: str = RecordType.SESSION_START.value
    session_id: Optional[str] = None
    task_id: Optional[str] = None
    task_label: Optional[str] = None
    duration_s: Optional[float] = None
    idle_since: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        # Strip None for compactness
        return {k: v for k, v in d.items() if v is not None or k in ("metadata",)}


# ---------------------------------------------------------------------------
# Tracker
# ---------------------------------------------------------------------------

class TCPTracker:
    """Main tracker class — call methods from your session/task hooks."""

    def __init__(
        self,
        storage_dir: Optional[Path] = None,
        checkpoint_interval: int = CHECKPOINT_INTERVAL_S,
        idle_threshold: int = IDLE_THRESHOLD_S,
    ):
        self.storage_dir = storage_dir or STORAGE_DIR
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoint_interval = checkpoint_interval
        self.idle_threshold = idle_threshold

        self.session_id: Optional[str] = None
        self.current_task_id: Optional[str] = None
        self.current_task_label: Optional[str] = None
        self.task_start_ts: Optional[float] = None
        self.last_activity_ts: float = time.time()
        self.is_idle: bool = False
        self.idle_start_ts: Optional[float] = None
        self._checkpoint_due_ts: float = 0.0

    # ---- Session lifecycle ----

    def start_session(self, metadata: Optional[dict[str, Any]] = None) -> str:
        """Begin a new work session. Returns the session_id."""
        self.session_id = f"sess-{uuid.uuid4().hex[:12]}"
        rec = Record(
            type=RecordType.SESSION_START.value,
            session_id=self.session_id,
            metadata=metadata or {},
        )
        _atomic_append(_daily_log_path(), rec.to_dict())
        self._checkpoint_due_ts = time.time() + self.checkpoint_interval
        self.last_activity_ts = time.time()
        return self.session_id

    def end_session(self, metadata: Optional[dict[str, Any]] = None) -> None:
        """Close the current session, flushing any open task."""
        if self.current_task_id:
            self.end_task(metadata=metadata)
        if not self.session_id:
            return
        rec = Record(
            type=RecordType.SESSION_END.value,
            session_id=self.session_id,
            metadata=metadata or {},
        )
        _atomic_append(_daily_log_path(), rec.to_dict())
        self.session_id = None

    # ---- Task lifecycle ----

    def start_task(self, label: str, metadata: Optional[dict[str, Any]] = None) -> str:
        """Start work on a new task. Auto-ends any in-progress task."""
        if self.current_task_id:
            self.end_task(metadata={"reason": "auto_switch", **(metadata or {})})
        if not self.session_id:
            self.start_session()

        task_id = f"task-{uuid.uuid4().hex[:10]}"
        self.current_task_id = task_id
        self.current_task_label = label
        self.task_start_ts = time.time()
        self.last_activity_ts = self.task_start_ts

        rec = Record(
            type=RecordType.TASK_START.value,
            session_id=self.session_id,
            task_id=task_id,
            task_label=label,
            metadata=metadata or {},
        )
        _atomic_append(_daily_log_path(), rec.to_dict())
        return task_id

    def end_task(self, metadata: Optional[dict[str, Any]] = None) -> Optional[float]:
        """End the current task. Returns duration in seconds."""
        if not self.current_task_id or self.task_start_ts is None:
            return None
        duration = time.time() - self.task_start_ts
        rec = Record(
            type=RecordType.TASK_END.value,
            session_id=self.session_id,
            task_id=self.current_task_id,
            task_label=self.current_task_label,
            duration_s=round(duration, 2),
            metadata=metadata or {},
        )
        _atomic_append(_daily_log_path(), rec.to_dict())
        self.current_task_id = None
        self.current_task_label = None
        self.task_start_ts = None
        return duration

    # ---- Activity heartbeat ----

    def heartbeat(self) -> Optional[dict[str, Any]]:
        """
        Call periodically (e.g., before/after each tool call).
        Returns a record dict if a checkpoint was emitted, else None.
        """
        now = time.time()
        self.last_activity_ts = now

        # Wake from idle?
        if self.is_idle:
            self._end_idle(now)

        # Check if checkpoint is due
        if now >= self._checkpoint_due_ts:
            return self._emit_checkpoint(now)
        return None

    # ---- Idle detection ----

    def check_idle(self) -> Optional[dict[str, Any]]:
        """Call periodically to detect idle state. Returns idle_start record if newly idle."""
        now = time.time()
        if self.is_idle:
            return None
        if now - self.last_activity_ts >= self.idle_threshold:
            self._start_idle(now)
            return self._read_last_record()
        return None

    def _start_idle(self, now: float) -> None:
        self.is_idle = True
        self.idle_start_ts = now
        rec = Record(
            type=RecordType.IDLE_START.value,
            session_id=self.session_id,
            task_id=self.current_task_id,
            task_label=self.current_task_label,
            idle_since=_now_iso(),
        )
        _atomic_append(_daily_log_path(), rec.to_dict())

    def _end_idle(self, now: float) -> None:
        duration = round(now - (self.idle_start_ts or now), 2)
        rec = Record(
            type=RecordType.IDLE_END.value,
            session_id=self.session_id,
            task_id=self.current_task_id,
            task_label=self.current_task_label,
            duration_s=duration,
        )
        _atomic_append(_daily_log_path(), rec.to_dict())
        self.is_idle = False
        self.idle_start_ts = None

    # ---- Checkpoints ----

    def _emit_checkpoint(self, now: float) -> dict[str, Any]:
        rec = Record(
            type=RecordType.CHECKPOINT.value,
            session_id=self.session_id,
            task_id=self.current_task_id,
            task_label=self.current_task_label,
            duration_s=round(now - (self.task_start_ts or now), 2) if self.task_start_ts else 0,
        )
        d = rec.to_dict()
        _atomic_append(_daily_log_path(), d)
        self._checkpoint_due_ts = now + self.checkpoint_interval
        return d

    # ---- Daily summary ----

    @classmethod
    def generate_daily_summary(cls, day: Optional[str] = None) -> dict[str, Any]:
        """Read all records for `day` and produce a summary record."""
        day = day or _today_str()
        log_path = STORAGE_DIR / f"tcp_{day}.jsonl"
        if not log_path.exists():
            return {}

        records: list[dict[str, Any]] = []
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue

        session_starts = [r for r in records if r.get("type") == RecordType.SESSION_START.value]
        session_ends = [r for r in records if r.get("type") == RecordType.SESSION_END.value]
        tasks = [r for r in records if r.get("type") == RecordType.TASK_END.value]
        idles = [r for r in records if r.get("type") == RecordType.IDLE_END.value]
        checkpoints = [r for r in records if r.get("type") == RecordType.CHECKPOINT.value]

        total_work_s = sum(r.get("duration_s", 0) or 0 for r in tasks)
        total_idle_s = sum(r.get("duration_s", 0) or 0 for r in idles)
        task_labels: dict[str, float] = {}
        for t in tasks:
            label = t.get("task_label") or t.get("task_id", "unknown")
            task_labels[label] = task_labels.get(label, 0) + (t.get("duration_s", 0) or 0)

        summary = {
            "record_id": uuid.uuid4().hex[:16],
            "timestamp": _now_iso(),
            "type": RecordType.DAILY_SUMMARY.value,
            "session_count": len(session_starts),
            "total_work_s": round(total_work_s, 2),
            "total_work_h": round(total_work_s / 3600, 2),
            "total_idle_s": round(total_idle_s, 2),
            "total_idle_h": round(total_idle_s / 3600, 2),
            "tasks_completed": len(tasks),
            "tasks": {k: round(v, 2) for k, v in task_labels.items()},
            "checkpoints": len(checkpoints),
            "idle_episodes": len(idles),
            "day": day,
        }

        # Append summary to the same daily log
        _atomic_append(log_path, summary)
        return summary

    # ---- Introspection ----

    def get_status(self) -> dict[str, Any]:
        now = time.time()
        return {
            "session_id": self.session_id,
            "current_task": self.current_task_label,
            "task_id": self.current_task_id,
            "is_idle": self.is_idle,
            "task_elapsed_s": round(now - self.task_start_ts, 2) if self.task_start_ts else 0,
            "idle_for_s": round(now - self.idle_start_ts, 2) if self.is_idle and self.idle_start_ts else 0,
            "next_checkpoint_in_s": max(0, round(self._checkpoint_due_ts - now, 2)),
            "storage_dir": str(self.storage_dir),
        }

    def _read_last_record(self) -> dict[str, Any]:
        log_path = _daily_log_path()
        if not log_path.exists():
            return {}
        with open(log_path, "rb") as f:
            f.seek(0, 2)
            if f.tell() == 0:
                return {}
            f.seek(-1, 2)
            # Read last line
            while f.tell() > 0 and f.read(1) != b"\n":
                f.seek(-2, 1)
            line = f.readline().decode("utf-8").strip()
        return json.loads(line) if line else {}


# ---------------------------------------------------------------------------
# CLI / Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Simple CLI demo: start session, simulate tasks, idle, checkpoint, summary."""
    import argparse

    parser = argparse.ArgumentParser(description="TCP Work-Time Tracker")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("session-start", help="Begin a new work session")
    sub.add_parser("session-end", help="End the current session")

    p_task = sub.add_parser("task-start", help="Start a task")
    p_task.add_argument("label", help="Task label/description")

    sub.add_parser("task-end", help="End the current task")
    sub.add_parser("status", help="Print current tracker status")
    sub.add_parser("summary", help="Generate daily summary")

    args = parser.parse_args()
    tracker = TCPTracker()

    if args.command == "session-start":
        sid = tracker.start_session()
        print(f"Session started: {sid}")
    elif args.command == "session-end":
        tracker.end_session()
        print("Session ended.")
    elif args.command == "task-start":
        tid = tracker.start_task(args.label)
        print(f"Task started: {tid} — {args.label}")
    elif args.command == "task-end":
        d = tracker.end_task()
        print(f"Task ended. Duration: {d:.1f}s" if d else "No active task.")
    elif args.command == "status":
        print(json.dumps(tracker.get_status(), indent=2))
    elif args.command == "summary":
        s = TCPTracker.generate_daily_summary()
        print(json.dumps(s, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
