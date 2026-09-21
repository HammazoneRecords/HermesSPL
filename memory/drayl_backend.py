"""Fork-local active Drayl archive.

The archive is append-only: events and provenance receipts are immutable rows.
Snapshots are retained for every observation, including unchanged observations.
No network, credentials, or live-workspace paths are used.
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import time
import uuid
from pathlib import Path
from typing import Any, Iterable

ARCHIVE_NAMESPACE = "TRIANGULUM/ANDROMALIUS"


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _digest(value: Any) -> str:
    return hashlib.sha256(_json(value).encode("utf-8")).hexdigest()


class DraylBackend:
    """SQLite-backed, source-linked archive with deterministic receipts."""

    def __init__(self, path: str | Path = ":memory:") -> None:
        self.path = str(path)
        self.db = sqlite3.connect(self.path)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys = ON")
        self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS events (
                event_id TEXT PRIMARY KEY, source_id TEXT NOT NULL, source_ref TEXT NOT NULL,
                payload TEXT NOT NULL, payload_hash TEXT NOT NULL, tags TEXT NOT NULL,
                changed INTEGER NOT NULL, observed_at REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS snapshots (
                snapshot_id TEXT PRIMARY KEY, source_id TEXT NOT NULL, event_id TEXT NOT NULL,
                payload TEXT NOT NULL, payload_hash TEXT NOT NULL, changed INTEGER NOT NULL,
                observed_at REAL NOT NULL, FOREIGN KEY(event_id) REFERENCES events(event_id)
            );
            CREATE TABLE IF NOT EXISTS receipts (
                receipt_id TEXT PRIMARY KEY, event_id TEXT NOT NULL, receipt TEXT NOT NULL,
                receipt_hash TEXT NOT NULL, FOREIGN KEY(event_id) REFERENCES events(event_id)
            );
            CREATE INDEX IF NOT EXISTS idx_events_source ON events(source_id);
            CREATE INDEX IF NOT EXISTS idx_snapshots_source ON snapshots(source_id);
            """
        )
        self.db.commit()

    def append(self, source_id: str, payload: Any, *, source_ref: str | None = None,
               tags: Iterable[str] = ()) -> dict[str, Any]:
        """Append one observation and its receipt; never overwrite an event."""
        if not source_id or not isinstance(source_id, str):
            raise ValueError("source_id must be a non-empty string")
        source_ref = source_ref or source_id
        tag_list = sorted({str(tag) for tag in tags})
        payload_hash = _digest(payload)
        previous = self.db.execute(
            "SELECT payload_hash FROM snapshots WHERE source_id=? ORDER BY observed_at DESC LIMIT 1",
            (source_id,),
        ).fetchone()
        changed = previous is None or previous["payload_hash"] != payload_hash
        now = time.time()
        event_id = uuid.uuid4().hex
        snapshot_id = uuid.uuid4().hex
        receipt_id = uuid.uuid4().hex
        event = {"event_id": event_id, "source_id": source_id, "source_ref": source_ref,
                 "payload_hash": payload_hash, "changed": changed, "tags": tag_list,
                 "namespace": ARCHIVE_NAMESPACE, "observed_at": now}
        receipt_hash = _digest(event)
        receipt = {**event, "receipt_id": receipt_id, "receipt_hash": receipt_hash}
        with self.db:
            self.db.execute("INSERT INTO events VALUES (?,?,?,?,?,?,?,?)",
                            (event_id, source_id, source_ref, _json(payload), payload_hash,
                             _json(tag_list), int(changed), now))
            self.db.execute("INSERT INTO snapshots VALUES (?,?,?,?,?,?,?)",
                            (snapshot_id, source_id, event_id, _json(payload), payload_hash,
                             int(changed), now))
            self.db.execute("INSERT INTO receipts VALUES (?,?,?,?)",
                            (receipt_id, event_id, _json(receipt), receipt_hash))
        return {"event_id": event_id, "snapshot_id": snapshot_id, "changed": changed,
                "payload_hash": payload_hash, "receipt_id": receipt_id,
                "receipt_hash": receipt_hash, "namespace": ARCHIVE_NAMESPACE}

    def snapshot(self, source_id: str, *, latest: bool = True) -> dict[str, Any] | list[dict[str, Any]] | None:
        sql = "SELECT * FROM snapshots WHERE source_id=? ORDER BY observed_at"
        rows = [dict(row) for row in self.db.execute(sql, (source_id,)).fetchall()]
        for row in rows:
            row["payload"] = json.loads(row["payload"])
            row["changed"] = bool(row["changed"])
        return (rows[-1] if rows else None) if latest else rows

    def query(self, text: str = "", *, limit: int = 20) -> list[dict[str, Any]]:
        """Return source-linked events ranked by lexical token resonance."""
        tokens = set(re.findall(r"[\w-]+", text.casefold()))
        rows = self.db.execute("SELECT * FROM events ORDER BY observed_at DESC").fetchall()
        results = []
        for row in rows:
            haystack = " ".join((row["source_id"], row["source_ref"], row["payload"], row["tags"])).casefold()
            score = sum(token in haystack for token in tokens) if tokens else 1
            if score:
                item = dict(row)
                item.update(payload=json.loads(row["payload"]), tags=json.loads(row["tags"]),
                            changed=bool(row["changed"]), resonance=score)
                results.append(item)
        return sorted(results, key=lambda item: (-item["resonance"], -item["observed_at"]))[:limit]

    def receipt(self, event_id: str) -> dict[str, Any] | None:
        row = self.db.execute("SELECT receipt FROM receipts WHERE event_id=?", (event_id,)).fetchone()
        return json.loads(row["receipt"]) if row else None

    def close(self) -> None:
        self.db.close()

    def __enter__(self) -> "DraylBackend":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()
