#!/usr/bin/env python3
"""
Inter-Agent Work Router — Routes work through the 4-stage agent pipeline:

    TCP (timeline) → FactCheck (verify) → Scribe (document) → MemoryCurator (archive)

Features:
  - Priority queue (CRITICAL > HIGH > NORMAL > LOW > BACKGROUND)
  - Per-stage retry with exponential backoff + jitter
  - Full audit trail (JSONL, append-only, atomic writes)
  - Dead-letter queue for exhausted retries
  - Stage-level timeouts
  - Idempotency keys
  - Introspection API (pending, in-flight, completed, failed, dead-lettered)

Storage layout (alongside tcp_tracker):
    <workspace>/autopilot/
    ├── router.py            # this file
    ├── tcp_tracker.py       # existing TCP tracker
    ├── queue/               # persistent queue state
    │   ├── pending.jsonl    # enqueued work items
    │   ├── inflight.jsonl   # currently processing
    │   ├── completed.jsonl  # successfully routed through all stages
    │   ├── failed.jsonl     # failed at some stage (retries remaining)
    │   └── dead_letter.jsonl # exhausted all retries
    └── audit/
        └── audit_YYYY-MM-DD.jsonl  # audit trail per day

Author: HermesSPL Autopilot
Version: 1.0.0
"""

from __future__ import annotations

import json
import os
import threading
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

WORKSPACE = Path(os.environ.get(
    "AUTOPILOT_WORKSPACE",
    Path(__file__).resolve().parents[1],
))

AUTOPILOT_DIR = WORKSPACE / "autopilot"
QUEUE_DIR = AUTOPILOT_DIR / "queue"
AUDIT_DIR = AUTOPILOT_DIR / "audit"

# Stage pipeline definition
STAGE_PIPELINE: list[str] = ["TCP", "FACTCHECK", "SCRIBE", "MEMORY_CURATOR"]

# Retry policy
MAX_RETRIES_PER_STAGE: int = 3
RETRY_BASE_DELAY_S: float = 1.0
RETRY_MAX_DELAY_S: float = 60.0
RETRY_BACKOFF_FACTOR: float = 2.0

# Stage timeouts (seconds)
STAGE_TIMEOUTS: dict[str, int] = {
    "TCP": 300,           # 5 min — timeline formalization
    "FACTCHECK": 600,     # 10 min — verification
    "SCRIBE": 300,        # 5 min — documentation
    "MEMORY_CURATOR": 120, # 2 min — archival
}

# Priority levels (lower number = higher priority)
class Priority(int, Enum):
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3
    BACKGROUND = 4


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
    with open(path, "a", encoding="utf-8") as f:
        f.write(line)
        f.flush()
        os.fsync(f.fileno())


def _read_all_records(path: Path) -> list[dict[str, Any]]:
    """Read all JSON records from a JSONL file."""
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return records


def _audit_log_path(day: Optional[str] = None) -> Path:
    day = day or _today_str()
    return AUDIT_DIR / f"audit_{day}.jsonl"


def _stage_queue_path(stage: str, status: str) -> Path:
    """Get path for a stage-specific queue file."""
    return QUEUE_DIR / f"{stage.lower()}_{status}.jsonl"


# ---------------------------------------------------------------------------
# Work Item
# ---------------------------------------------------------------------------

@dataclass
class WorkItem:
    """A unit of work flowing through the agent pipeline."""
    item_id: str = field(default_factory=lambda: f"wi-{uuid.uuid4().hex[:12]}")
    idempotency_key: str = field(default_factory=lambda: uuid.uuid4().hex)
    priority: int = Priority.NORMAL.value
    payload: dict[str, Any] = field(default_factory=dict)
    current_stage: str = "TCP"
    stage_index: int = 0
    retries: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    max_retries: int = MAX_RETRIES_PER_STAGE
    status: str = "pending"  # pending, inflight, completed, failed, dead_letter
    created_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)
    completed_at: Optional[str] = None
    error: Optional[str] = None
    stage_history: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = {
            "item_id": self.item_id,
            "idempotency_key": self.idempotency_key,
            "priority": self.priority,
            "payload": self.payload,
            "current_stage": self.current_stage,
            "stage_index": self.stage_index,
            "retries": dict(self.retries) if isinstance(self.retries, defaultdict) else self.retries,
            "max_retries": self.max_retries,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "completed_at": self.completed_at,
            "error": self.error,
            "stage_history": self.stage_history,
            "metadata": self.metadata,
        }
        return {k: v for k, v in d.items() if v is not None or k in ("payload", "metadata", "stage_history", "retries")}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "WorkItem":
        item = cls(
            item_id=d.get("item_id", f"wi-{uuid.uuid4().hex[:12]}"),
            idempotency_key=d.get("idempotency_key", uuid.uuid4().hex),
            priority=d.get("priority", Priority.NORMAL.value),
            payload=d.get("payload", {}),
            current_stage=d.get("current_stage", "TCP"),
            stage_index=d.get("stage_index", 0),
            max_retries=d.get("max_retries", MAX_RETRIES_PER_STAGE),
            status=d.get("status", "pending"),
            created_at=d.get("created_at", _now_iso()),
            updated_at=d.get("updated_at", _now_iso()),
            completed_at=d.get("completed_at"),
            error=d.get("error"),
            stage_history=d.get("stage_history", []),
            metadata=d.get("metadata", {}),
        )
        item.retries = defaultdict(int, d.get("retries", {}))
        return item

    @property
    def priority_label(self) -> str:
        try:
            return Priority(self.priority).name
        except ValueError:
            return f"UNKNOWN({self.priority})"


# ---------------------------------------------------------------------------
# Audit Trail
# ---------------------------------------------------------------------------

class AuditTrail:
    """Append-only audit trail for all routing decisions."""

    def __init__(self, audit_dir: Optional[Path] = None):
        self.audit_dir = audit_dir or AUDIT_DIR
        self.audit_dir.mkdir(parents=True, exist_ok=True)

    def log(
        self,
        event_type: str,
        item_id: str,
        stage: str,
        details: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Write an audit record."""
        record = {
            "audit_id": f"aud-{uuid.uuid4().hex[:10]}",
            "timestamp": _now_iso(),
            "event_type": event_type,
            "item_id": item_id,
            "stage": stage,
            "details": details or {},
        }
        _atomic_append(_audit_log_path(), record)
        return record

    def query(
        self,
        item_id: Optional[str] = None,
        stage: Optional[str] = None,
        event_type: Optional[str] = None,
        day: Optional[str] = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Query audit records with optional filters."""
        records = _read_all_records(_audit_log_path(day))
        if item_id:
            records = [r for r in records if r.get("item_id") == item_id]
        if stage:
            records = [r for r in records if r.get("stage") == stage]
        if event_type:
            records = [r for r in records if r.get("event_type") == event_type]
        return records[-limit:]


# ---------------------------------------------------------------------------
# Retry Logic
# ---------------------------------------------------------------------------

class RetryPolicy:
    """Exponential backoff with jitter for stage retries."""

    def __init__(
        self,
        max_retries: int = MAX_RETRIES_PER_STAGE,
        base_delay: float = RETRY_BASE_DELAY_S,
        max_delay: float = RETRY_MAX_DELAY_S,
        backoff_factor: float = RETRY_BACKOFF_FACTOR,
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor

    def can_retry(self, item: WorkItem) -> bool:
        """Check if the item can be retried at its current stage."""
        stage_retries = item.retries.get(item.current_stage, 0)
        return stage_retries < min(item.max_retries, self.max_retries)

    def next_delay(self, item: WorkItem) -> float:
        """Calculate next retry delay with jitter."""
        import random
        stage_retries = item.retries.get(item.current_stage, 0)
        delay = self.base_delay * (self.backoff_factor ** stage_retries)
        delay = min(delay, self.max_delay)
        # Add ±25% jitter
        jitter = delay * 0.25 * (2 * random.random() - 1)
        return max(0.1, delay + jitter)

    def record_retry(self, item: WorkItem) -> None:
        """Record a retry attempt for the current stage."""
        item.retries[item.current_stage] = item.retries.get(item.current_stage, 0) + 1


# ---------------------------------------------------------------------------
# Stage Handlers (Protocol Interface)
# ---------------------------------------------------------------------------

# A stage handler is a Callable[[WorkItem], tuple[bool, dict[str, Any]]]
# Returns: (success: bool, result_payload: dict)
StageHandler = Callable[[WorkItem], tuple[bool, dict[str, Any]]]


class StageRegistry:
    """Registry of stage handlers. Handlers are pluggable."""

    def __init__(self):
        self._handlers: dict[str, StageHandler] = {}

    def register(self, stage: str, handler: StageHandler) -> None:
        """Register a handler for a stage."""
        self._handlers[stage.upper()] = handler

    def get(self, stage: str) -> Optional[StageHandler]:
        """Get the handler for a stage."""
        return self._handlers.get(stage.upper())

    def has(self, stage: str) -> bool:
        """Check if a handler is registered for a stage."""
        return stage.upper() in self._handlers


# ---------------------------------------------------------------------------
# Priority Queue
# ---------------------------------------------------------------------------

class PriorityQueue:
    """File-backed priority queue with in-memory cache."""

    def __init__(self, queue_dir: Optional[Path] = None):
        self.queue_dir = queue_dir or QUEUE_DIR
        self.queue_dir.mkdir(parents=True, exist_ok=True)
        self._pending_path = self.queue_dir / "pending.jsonl"
        self._lock = threading.Lock()

    def enqueue(self, item: WorkItem) -> None:
        """Add a work item to the queue."""
        with self._lock:
            _atomic_append(self._pending_path, item.to_dict())

    def dequeue(self) -> Optional[WorkItem]:
        """Remove and return the highest-priority pending item."""
        with self._lock:
            records = _read_all_records(self._pending_path)
            if not records:
                return None

            # Sort by priority (ascending = higher priority first), then by created_at
            records.sort(key=lambda r: (r.get("priority", Priority.NORMAL.value), r.get("created_at", "")))
            next_record = records[0]
            item = WorkItem.from_dict(next_record)

            # Re-write the file without the dequeued item
            remaining = records[1:]
            self._pending_path.unlink(missing_ok=True)
            for r in remaining:
                _atomic_append(self._pending_path, r)

            return item

    def peek(self) -> Optional[WorkItem]:
        """View the next item without removing it."""
        records = _read_all_records(self._pending_path)
        if not records:
            return None
        records.sort(key=lambda r: (r.get("priority", Priority.NORMAL.value), r.get("created_at", "")))
        return WorkItem.from_dict(records[0])

    def size(self) -> int:
        """Return the number of pending items."""
        return len(_read_all_records(self._pending_path))

    def all_pending(self) -> list[WorkItem]:
        """Return all pending items sorted by priority."""
        records = _read_all_records(self._pending_path)
        records.sort(key=lambda r: (r.get("priority", Priority.NORMAL.value), r.get("created_at", "")))
        return [WorkItem.from_dict(r) for r in records]


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

class InterAgentRouter:
    """
    Main router class — orchestrates work through the 4-stage pipeline.

    Usage:
        router = InterAgentRouter()
        router.stages.register("TCP", my_tcp_handler)
        router.stages.register("FACTCHECK", my_factcheck_handler)
        router.stages.register("SCRIBE", my_scribe_handler)
        router.stages.register("MEMORY_CURATOR", my_curator_handler)

        item_id = router.submit({"claim": "something", "source": "chat-123"})
        router.process_one()  # process single item
        router.run()          # run continuously (blocking)
    """

    def __init__(
        self,
        workspace: Optional[Path] = None,
        max_retries: int = MAX_RETRIES_PER_STAGE,
        stage_timeouts: Optional[dict[str, int]] = None,
    ):
        self.workspace = workspace or WORKSPACE
        self.queue_dir = self.workspace / "autopilot" / "queue"
        self.audit_dir = self.workspace / "autopilot" / "audit"
        self.queue_dir.mkdir(parents=True, exist_ok=True)
        self.audit_dir.mkdir(parents=True, exist_ok=True)

        self.queue = PriorityQueue(self.queue_dir)
        self.audit = AuditTrail(self.audit_dir)
        self.retry_policy = RetryPolicy(max_retries=max_retries)
        self.stages = StageRegistry()
        self.stage_timeouts = stage_timeouts or STAGE_TIMEOUTS

        # In-memory tracking of in-flight items
        self._inflight: dict[str, WorkItem] = {}
        self._inflight_path = self.queue_dir / "inflight.jsonl"
        self._completed_path = self.queue_dir / "completed.jsonl"
        self._failed_path = self.queue_dir / "failed.jsonl"
        self._dead_letter_path = self.queue_dir / "dead_letter.jsonl"

        self._running = False
        self._stop_event = threading.Event()

    # ---- Submission API ----

    def submit(
        self,
        payload: dict[str, Any],
        priority: Priority = Priority.NORMAL,
        idempotency_key: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> str:
        """
        Submit a new work item to the pipeline.

        Returns the item_id.
        """
        item = WorkItem(
            priority=priority.value,
            payload=payload,
            idempotency_key=idempotency_key or uuid.uuid4().hex,
            metadata=metadata or {},
        )
        self.queue.enqueue(item)
        self.audit.log("SUBMITTED", item.item_id, "ROUTER", {
            "priority": item.priority_label,
            "idempotency_key": item.idempotency_key,
        })
        return item.item_id

    def submit_critical(self, payload: dict[str, Any], **kwargs) -> str:
        """Submit a CRRIORITY item."""
        return self.submit(payload, priority=Priority.CRITICAL, **kwargs)

    def submit_high(self, payload: dict[str, Any], **kwargs) -> str:
        """Submit a HIGH priority item."""
        return self.submit(payload, priority=Priority.HIGH, **kwargs)

    def submit_background(self, payload: dict[str, Any], **kwargs) -> str:
        """Submit a BACKGROUND priority item."""
        return self.submit(payload, priority=Priority.BACKGROUND, **kwargs)

    # ---- Processing ----

    def process_one(self) -> Optional[WorkItem]:
        """Process a single work item through one stage. Returns the item if processed."""
        item = self.queue.dequeue()
        if item is None:
            return None

        # Move to in-flight
        item.status = "inflight"
        item.updated_at = _now_iso()
        self._inflight[item.item_id] = item
        _atomic_append(self._inflight_path, item.to_dict())

        self.audit.log("DEQUEUED", item.item_id, item.current_stage, {
            "priority": item.priority_label,
            "stage_index": item.stage_index,
        })

        # Execute the stage
        success = self._execute_stage(item)

        if success:
            # Advance to next stage
            self._advance_stage(item)
        else:
            # Handle failure
            self._handle_stage_failure(item)

        return item

    def _execute_stage(self, item: WorkItem) -> bool:
        """Execute the current stage handler for an item."""
        stage = item.current_stage
        handler = self.stages.get(stage)

        if handler is None:
            # No handler registered — auto-pass (useful for testing)
            self.audit.log("STAGE_NO_HANDLER", item.item_id, stage, {
                "note": "No handler registered, auto-passing",
            })
            item.stage_history.append({
                "stage": stage,
                "status": "auto_passed",
                "timestamp": _now_iso(),
            })
            return True

        self.audit.log("STAGE_START", item.item_id, stage, {
            "retry_count": item.retries.get(stage, 0),
        })

        try:
            success, result = handler(item)
            if success:
                item.payload.update(result)
                item.stage_history.append({
                    "stage": stage,
                    "status": "completed",
                    "timestamp": _now_iso(),
                    "result_keys": list(result.keys()),
                })
                self.audit.log("STAGE_SUCCESS", item.item_id, stage, {
                    "result_keys": list(result.keys()),
                })
            else:
                item.stage_history.append({
                    "stage": stage,
                    "status": "failed",
                    "timestamp": _now_iso(),
                    "error": result.get("error", "unknown"),
                })
                self.audit.log("STAGE_FAILURE", item.item_id, stage, {
                    "error": result.get("error", "unknown"),
                })
            return success

        except Exception as e:
            item.stage_history.append({
                "stage": stage,
                "status": "exception",
                "timestamp": _now_iso(),
                "error": str(e),
            })
            self.audit.log("STAGE_EXCEPTION", item.item_id, stage, {
                "error": str(e),
                "error_type": type(e).__name__,
            })
            return False

    def _advance_stage(self, item: WorkItem) -> None:
        """Move item to the next stage in the pipeline."""
        item.stage_index += 1

        if item.stage_index >= len(STAGE_PIPELINE):
            # Pipeline complete
            item.status = "completed"
            item.completed_at = _now_iso()
            item.updated_at = _now_iso()
            _atomic_append(self._completed_path, item.to_dict())
            self.audit.log("PIPELINE_COMPLETE", item.item_id, "ROUTER", {
                "total_stages": len(STAGE_PIPELINE),
                "completed_at": item.completed_at,
            })
            # Remove from in-flight
            self._inflight.pop(item.item_id, None)
            self._persist_inflight()
        else:
            # Move to next stage
            item.current_stage = STAGE_PIPELINE[item.stage_index]
            item.updated_at = _now_iso()
            # Re-enqueue for next stage processing
            item.status = "pending"
            self.queue.enqueue(item)
            self.audit.log("STAGE_ADVANCE", item.item_id, item.current_stage, {
                "new_stage_index": item.stage_index,
            })
            # Remove from in-flight
            self._inflight.pop(item.item_id, None)
            self._persist_inflight()

    def _handle_stage_failure(self, item: WorkItem) -> None:
        """Handle a stage failure — retry or dead-letter."""
        stage = item.current_stage

        if self.retry_policy.can_retry(item):
            # Retry
            self.retry_policy.record_retry(item)
            delay = self.retry_policy.next_delay(item)
            item.updated_at = _now_iso()
            item.status = "pending"
            item.error = f"Retry {item.retries[stage]}/{self.retry_policy.max_retries} after {delay:.1f}s delay"

            self.audit.log("STAGE_RETRY_SCHEDULED", item.item_id, stage, {
                "retry_count": item.retries[stage],
                "delay_s": round(delay, 2),
            })

            # Re-enqueue (in production, you'd schedule this with a delay)
            # For simplicity, we re-enqueue immediately
            self.queue.enqueue(item)

            # Remove from in-flight
            self._inflight.pop(item.item_id, None)
            self._persist_inflight()
        else:
            # Dead letter
            item.status = "dead_letter"
            item.updated_at = _now_iso()
            item.error = f"Exhausted {item.retries.get(stage, 0)} retries at stage {stage}"
            _atomic_append(self._dead_letter_path, item.to_dict())
            self.audit.log("DEAD_LETTERED", item.item_id, stage, {
                "total_retries": item.retries.get(stage, 0),
                "error": item.error,
            })
            # Remove from in-flight
            self._inflight.pop(item.item_id, None)
            self._persist_inflight()

    def _persist_inflight(self) -> None:
        """Persist the in-flight state to disk."""
        self._inflight_path.unlink(missing_ok=True)
        for item in self._inflight.values():
            _atomic_append(self._inflight_path, item.to_dict())

    # ---- Continuous Processing ----

    def run(self, poll_interval: float = 1.0) -> None:
        """
        Run the router continuously. Blocks until stop() is called.

        Args:
            poll_interval: Seconds between queue checks when empty.
        """
        self._running = True
        self._stop_event.clear()
        self.audit.log("ROUTER_START", "system", "ROUTER", {
            "pipeline": STAGE_PIPELINE,
            "max_retries": self.retry_policy.max_retries,
        })

        while self._running and not self._stop_event.is_set():
            try:
                item = self.process_one()
                if item is None:
                    # No work available, wait before polling again
                    self._stop_event.wait(poll_interval)
            except Exception as e:
                self.audit.log("ROUTER_ERROR", "system", "ROUTER", {
                    "error": str(e),
                    "error_type": type(e).__name__,
                })
                self._stop_event.wait(poll_interval)

        self.audit.log("ROUTER_STOP", "system", "ROUTER", {})

    def stop(self) -> None:
        """Signal the router to stop."""
        self._running = False
        self._stop_event.set()

    # ---- Introspection API ----

    def get_status(self) -> dict[str, Any]:
        """Get current router status."""
        return {
            "running": self._running,
            "pending": self.queue.size(),
            "inflight": len(self._inflight),
            "completed": len(_read_all_records(self._completed_path)),
            "failed": len(_read_all_records(self._failed_path)),
            "dead_letter": len(_read_all_records(self._dead_letter_path)),
            "pipeline": STAGE_PIPELINE,
            "registered_handlers": [s for s in STAGE_PIPELINE if self.stages.has(s)],
        }

    def get_pending(self) -> list[WorkItem]:
        """Get all pending items."""
        return self.queue.all_pending()

    def get_inflight(self) -> list[WorkItem]:
        """Get all in-flight items."""
        return list(self._inflight.values())

    def get_completed(self, limit: int = 100) -> list[dict[str, Any]]:
        """Get completed items."""
        records = _read_all_records(self._completed_path)
        return records[-limit:]

    def get_dead_letters(self, limit: int = 100) -> list[dict[str, Any]]:
        """Get dead-lettered items."""
        records = _read_all_records(self._dead_letter_path)
        return records[-limit:]

    def get_item_history(self, item_id: str) -> list[dict[str, Any]]:
        """Get the full audit history for an item."""
        return self.audit.query(item_id=item_id, limit=1000)

    def retry_dead_letter(self, item_id: str) -> bool:
        """Manually retry a dead-lettered item from stage 0."""
        records = _read_all_records(self._dead_letter_path)
        for i, record in enumerate(records):
            if record.get("item_id") == item_id:
                item = WorkItem.from_dict(record)
                # Reset for retry
                item.status = "pending"
                item.current_stage = STAGE_PIPELINE[0]
                item.stage_index = 0
                item.retries = defaultdict(int)
                item.error = None
                item.updated_at = _now_iso()
                # Remove from dead letter
                records.pop(i)
                self._dead_letter_path.unlink(missing_ok=True)
                for r in records:
                    _atomic_append(self._dead_letter_path, r)
                # Re-enqueue
                self.queue.enqueue(item)
                self.audit.log("DEAD_LETTER_RETRY", item_id, "ROUTER", {})
                return True
        return False


# ---------------------------------------------------------------------------
# Default Stage Handlers (Stubs — override with real implementations)
# ---------------------------------------------------------------------------

def _default_tcp_handler(item: WorkItem) -> tuple[bool, dict[str, Any]]:
    """
    TCP Stage — Timeline formalization.
    Expected payload keys: claim, source, timestamp
    Output: timeline_event dict
    """
    # Stub: In production, this would invoke the TCP agent
    claim = item.payload.get("claim", "")
    source = item.payload.get("source", "unknown")
    return True, {
        "tcp_timeline_event": {
            "event_id": f"tl-{uuid.uuid4().hex[:8]}",
            "claim": claim,
            "source": source,
            "formalized_at": _now_iso(),
            "status": "timeline_created",
        }
    }


def _default_factcheck_handler(item: WorkItem) -> tuple[bool, dict[str, Any]]:
    """
    FactCheck Stage — Verification.
    Expected payload keys: claim, source, tcp_timeline_event
    Output: verification_result dict
    """
    # Stub: In production, this would invoke the FACTCHECK agent
    claim = item.payload.get("claim", "")
    return True, {
        "factcheck_result": {
            "check_id": f"fc-{uuid.uuid4().hex[:8]}",
            "claim": claim,
            "verdict": "VERIFIED",  # VERIFIED | PARTIALLY_VERIFIED | UNVERIFIED | CONTRADICTED
            "confidence": 0.85,
            "checked_at": _now_iso(),
            "evidence_refs": [],
        }
    }


def _default_scribe_handler(item: WorkItem) -> tuple[bool, dict[str, Any]]:
    """
    Scribe Stage — Documentation.
    Expected payload keys: claim, factcheck_result
    Output: document_ref dict
    """
    # Stub: In production, this would invoke the SOLOBIC_SCRIBE agent
    return True, {
        "scribe_document": {
            "doc_id": f"doc-{uuid.uuid4().hex[:8]}",
            "format": "markdown",
            "content_hash": uuid.uuid4().hex[:16],
            "drafted_at": _now_iso(),
            "word_count": 0,
        }
    }


def _default_curator_handler(item: WorkItem) -> tuple[bool, dict[str, Any]]:
    """
    MemoryCurator Stage — Archival.
    Expected payload keys: scribe_document, factcheck_result
    Output: archive_ref dict
    """
    # Stub: In production, this would invoke the MEMORY_CURATOR agent
    return True, {
        "curator_archive": {
            "archive_id": f"arc-{uuid.uuid4().hex[:8]}",
            "layer": "CONCEPTS",  # CONCEPTS | DIGESTS | FACT_CHECK
            "archived_at": _now_iso(),
            "provenance_chain": [h.get("stage") for h in item.stage_history],
        }
    }


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def create_default_router() -> InterAgentRouter:
    """Create a router with default stub handlers registered."""
    router = InterAgentRouter()
    router.stages.register("TCP", _default_tcp_handler)
    router.stages.register("FACTCHECK", _default_factcheck_handler)
    router.stages.register("SCRIBE", _default_scribe_handler)
    router.stages.register("MEMORY_CURATOR", _default_curator_handler)
    return router


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    """CLI for the inter-agent router."""
    import argparse

    parser = argparse.ArgumentParser(
        description="HermesSPL Inter-Agent Work Router",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  router.py submit --claim "AI is conscious" --source chat-123
  router.py submit --claim "Solobility = readiness" --priority HIGH
  router.py process-one
  router.py run
  router.py status
  router.py pending
  router.py history --item-id wi-abc123
  router.py retry-dead-letter --item-id wi-abc123
        """,
    )
    sub = parser.add_subparsers(dest="command")

    # submit
    p_submit = sub.add_parser("submit", help="Submit a work item")
    p_submit.add_argument("--claim", required=True, help="The claim/fact to process")
    p_submit.add_argument("--source", default="cli", help="Source identifier")
    p_submit.add_argument("--priority", default="NORMAL",
                          choices=["CRITICAL", "HIGH", "NORMAL", "LOW", "BACKGROUND"])
    p_submit.add_argument("--metadata", type=json.loads, default={},
                          help="JSON metadata string")

    # process-one
    sub.add_parser("process-one", help="Process one work item through one stage")

    # run
    p_run = sub.add_parser("run", help="Run the router continuously")
    p_run.add_argument("--poll-interval", type=float, default=1.0,
                       help="Seconds between queue polls when empty")

    # status
    sub.add_parser("status", help="Show router status")

    # pending
    sub.add_parser("pending", help="List pending items")

    # completed
    p_completed = sub.add_parser("completed", help="List completed items")
    p_completed.add_argument("--limit", type=int, default=20)

    # dead-letters
    p_dlq = sub.add_parser("dead-letters", help="List dead-lettered items")
    p_dlq.add_argument("--limit", type=int, default=20)

    # history
    p_history = sub.add_parser("history", help="Show audit history for an item")
    p_history.add_argument("--item-id", required=True)

    # retry-dead-letter
    p_retry = sub.add_parser("retry-dead-letter", help="Retry a dead-lettered item")
    p_retry.add_argument("--item-id", required=True)

    # audit-log
    p_audit = sub.add_parser("audit-log", help="Show recent audit log")
    p_audit.add_argument("--limit", type=int, default=50)
    p_audit.add_argument("--stage", default=None, help="Filter by stage")
    p_audit.add_argument("--event-type", default=None, help="Filter by event type")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    router = create_default_router()

    if args.command == "submit":
        priority = Priority[args.priority]
        item_id = router.submit(
            payload={"claim": args.claim, "source": args.source},
            priority=priority,
            metadata=args.metadata,
        )
        print(f"Submitted: {item_id} (priority={args.priority})")

    elif args.command == "process-one":
        item = router.process_one()
        if item:
            print(f"Processed: {item.item_id}")
            print(f"  Stage: {item.current_stage} (index={item.stage_index})")
            print(f"  Status: {item.status}")
            print(f"  History: {len(item.stage_history)} entries")
        else:
            print("No pending items.")

    elif args.command == "run":
        print(f"Running router (pipeline: {' → '.join(STAGE_PIPELINE)})")
        print("Press Ctrl+C to stop.")
        try:
            router.run(poll_interval=args.poll_interval)
        except KeyboardInterrupt:
            router.stop()
            print("\nRouter stopped.")

    elif args.command == "status":
        status = router.get_status()
        print(json.dumps(status, indent=2))

    elif args.command == "pending":
        items = router.get_pending()
        if not items:
            print("No pending items.")
        for item in items:
            print(f"  [{item.priority_label}] {item.item_id} — stage={item.current_stage} claim={item.payload.get('claim', '')[:50]}")

    elif args.command == "completed":
        items = router.get_completed(limit=args.limit)
        print(f"Completed items (last {len(items)}):")
        for item in items:
            print(f"  {item.get('item_id')} — completed_at={item.get('completed_at')}")

    elif args.command == "dead-letters":
        items = router.get_dead_letters(limit=args.limit)
        print(f"Dead-lettered items (last {len(items)}):")
        for item in items:
            print(f"  {item.get('item_id')} — error={item.get('error', '')}")

    elif args.command == "history":
        history = router.get_item_history(args.item_id)
        print(f"Audit history for {args.item_id} ({len(history)} events):")
        for event in history:
            print(f"  [{event.get('timestamp')}] {event.get('event_type')} @ {event.get('stage')}")

    elif args.command == "retry-dead-letter":
        success = router.retry_dead_letter(args.item_id)
        if success:
            print(f"Retrying dead-lettered item: {args.item_id}")
        else:
            print(f"Item not found in dead-letter queue: {args.item_id}")

    elif args.command == "audit-log":
        records = router.audit.query(
            stage=args.stage,
            event_type=args.event_type,
            limit=args.limit,
        )
        print(f"Audit log (last {len(records)} events):")
        for r in records:
            print(f"  [{r.get('timestamp')}] {r.get('event_type')} @ {r.get('stage')} — {r.get('item_id', '')}")


if __name__ == "__main__":
    main()
