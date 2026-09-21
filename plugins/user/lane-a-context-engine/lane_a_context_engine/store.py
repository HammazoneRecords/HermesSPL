"""SQLite store for pins, memory bank, data dump, compression events, and retrieval events."""

import json
import re
import sqlite3
import time
import uuid
from typing import Any, Dict, List, Optional


class ContextMemoryStore:
    """SQLite-backed store for context engine data."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        """Create all required tables."""
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS pins (
                pin_id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                pin_type TEXT NOT NULL,
                source_message_id TEXT,
                reason TEXT,
                confidence REAL DEFAULT 0.8,
                status TEXT DEFAULT 'active',
                destination TEXT DEFAULT 'summary',
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS memory_bank (
                memory_id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                source_pin_id TEXT,
                source_message_id TEXT,
                importance REAL DEFAULT 0.5,
                readonly INTEGER DEFAULT 1,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS data_dump (
                dump_id TEXT PRIMARY KEY,
                session_id TEXT,
                source_message_id TEXT,
                raw_content TEXT,
                summary TEXT,
                entities_json TEXT,
                retrieval_triggers_json TEXT,
                compression_event_id TEXT,
                created_at REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS compression_events (
                event_id TEXT PRIMARY KEY,
                session_id TEXT,
                trigger TEXT,
                context_ratio REAL,
                messages_compressed_json TEXT,
                protected_json TEXT,
                pins_json TEXT,
                risk_level TEXT,
                risk_reason TEXT,
                timestamp REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS retrieval_events (
                event_id TEXT PRIMARY KEY,
                dump_id TEXT,
                memory_id TEXT,
                trigger TEXT,
                relevance_score REAL,
                timestamp REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS integrity_reports (
                report_id TEXT PRIMARY KEY,
                event_id TEXT,
                checked_pins INTEGER,
                preserved_correctly INTEGER,
                weakened INTEGER,
                lost INTEGER,
                violations_json TEXT,
                timestamp REAL NOT NULL
            );
        """)
        self.conn.commit()

    def close(self):
        """Close the database connection."""
        self.conn.close()

    # ── Pins ─────────────────────────────────────────────────────────────

    def add_pin(self, pin_id: str, content: str, pin_type: str, source_message_id: str = "",
                reason: str = "", confidence: float = 0.8, destination: str = "summary"):
        """Add a pin to the store."""
        now = time.time()
        self.conn.execute(
            "INSERT INTO pins (pin_id, content, pin_type, source_message_id, reason, confidence, status, destination, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (pin_id, content, pin_type, source_message_id, reason, confidence, "active", destination, now, now),
        )
        self.conn.commit()

    def get_pin(self, pin_id: str) -> Optional[Dict[str, Any]]:
        """Get a pin by ID."""
        row = self.conn.execute("SELECT * FROM pins WHERE pin_id = ?", (pin_id,)).fetchone()
        return dict(row) if row else None

    def get_all_pins(self, status: str = "active") -> List[Dict[str, Any]]:
        """Get all pins with given status."""
        rows = self.conn.execute("SELECT * FROM pins WHERE status = ? ORDER BY created_at", (status,)).fetchall()
        return [dict(r) for r in rows]

    def unpin(self, pin_id: str):
        """Deactivate a pin."""
        self.conn.execute("UPDATE pins SET status = 'inactive', updated_at = ? WHERE pin_id = ?", (time.time(), pin_id))
        self.conn.commit()

    # ── Memory Bank ──────────────────────────────────────────────────────

    def add_memory(self, content: str, source_pin_id: str = None, source_message_id: str = None,
                   importance: float = 0.5) -> str:
        """Add an entry to the memory bank."""
        memory_id = f"mem_{uuid.uuid4().hex[:8]}"
        now = time.time()
        self.conn.execute(
            "INSERT INTO memory_bank (memory_id, content, source_pin_id, source_message_id, importance, readonly, created_at, updated_at) VALUES (?, ?, ?, ?, ?, 1, ?, ?)",
            (memory_id, content, source_pin_id, source_message_id, importance, now, now),
        )
        self.conn.commit()
        return memory_id

    def get_memory(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """Get a memory entry by ID."""
        row = self.conn.execute("SELECT * FROM memory_bank WHERE memory_id = ?", (memory_id,)).fetchone()
        return dict(row) if row else None

    def get_all_memory(self) -> List[Dict[str, Any]]:
        """Get all memory bank entries."""
        rows = self.conn.execute("SELECT * FROM memory_bank ORDER BY importance DESC, created_at").fetchall()
        return [dict(r) for r in rows]

    def search_memory(self, query: str) -> List[Dict[str, Any]]:
        """Search memory bank by keyword (matches any meaningful word in the query)."""
        stopwords = {"the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
                     "have", "has", "had", "do", "does", "did", "will", "would", "could",
                     "should", "may", "might", "can", "shall", "to", "of", "in", "for",
                     "on", "with", "at", "by", "from", "as", "into", "through", "during",
                     "before", "after", "above", "below", "between", "out", "off", "over",
                     "under", "again", "further", "then", "once", "and", "but", "or", "nor",
                     "not", "so", "than", "too", "very", "just", "about", "this", "that",
                     "these", "those", "it", "its", "i", "we", "you", "they", "he", "she",
                     "my", "your", "his", "her", "our", "their", "what", "which", "who",
                     "when", "where", "why", "how", "all", "each", "every", "both", "few",
                     "more", "most", "other", "some", "such", "no", "only", "own", "same",
                     "there", "here", "up", "down", "if", "because", "while", "although",
                     "until", "since", "however", "therefore", "thus", "hence", "tell",
                     "me", "about", "what", "how", "do", "does", "did"}
        words = [w for w in re.findall(r'\b[a-z]{3,}\b', query.lower()) if w not in stopwords]
        if not words:
            return []
        # Match any word in the query
        conditions = " OR ".join(["content LIKE ?"] * len(words))
        params = [f"%{w}%" for w in words]
        rows = self.conn.execute(
            f"SELECT * FROM memory_bank WHERE {conditions} ORDER BY importance DESC",
            params,
        ).fetchall()
        return [dict(r) for r in rows]

    # ── Data Dump ────────────────────────────────────────────────────────

    def add_to_dump(self, raw_content: str, summary: str = "", entities_json: str = "[]",
                    retrieval_triggers_json: str = "[]", compression_event_id: str = "",
                    session_id: str = "", source_message_id: str = "") -> str:
        """Add an entry to the data dump."""
        dump_id = f"dump_{uuid.uuid4().hex[:8]}"
        self.conn.execute(
            "INSERT INTO data_dump (dump_id, session_id, source_message_id, raw_content, summary, entities_json, retrieval_triggers_json, compression_event_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (dump_id, session_id, source_message_id, raw_content, summary, entities_json, retrieval_triggers_json, compression_event_id, time.time()),
        )
        self.conn.commit()
        return dump_id

    def get_dump_entry(self, dump_id: str) -> Optional[Dict[str, Any]]:
        """Get a data dump entry by ID."""
        row = self.conn.execute("SELECT * FROM data_dump WHERE dump_id = ?", (dump_id,)).fetchone()
        return dict(row) if row else None

    def get_all_dump(self) -> List[Dict[str, Any]]:
        """Get all data dump entries."""
        rows = self.conn.execute("SELECT * FROM data_dump ORDER BY created_at").fetchall()
        return [dict(r) for r in rows]

    def search_dump(self, query: str) -> List[Dict[str, Any]]:
        """Search data dump by keyword (matches any word in the query)."""
        words = re.findall(r'\b[a-z]{3,}\b', query.lower())
        if not words:
            return []
        conditions = " OR ".join(["raw_content LIKE ? OR summary LIKE ? OR entities_json LIKE ?"] * len(words))
        params = []
        for w in words:
            params.extend([f"%{w}%", f"%{w}%", f"%{w}%"])
        rows = self.conn.execute(
            f"SELECT * FROM data_dump WHERE {conditions}",
            params,
        ).fetchall()
        return [dict(r) for r in rows]

    def promote_dump_to_memory(self, dump_id: str, importance: float = 0.5) -> str:
        """Promote a data dump entry to the memory bank."""
        entry = self.get_dump_entry(dump_id)
        if not entry:
            raise ValueError(f"Dump entry not found: {dump_id}")
        memory_id = self.add_memory(
            content=entry["raw_content"],
            source_message_id=entry.get("source_message_id"),
            importance=importance,
        )
        return memory_id

    # ── Retrieval Events ─────────────────────────────────────────────────

    def record_retrieval(self, dump_id: str = None, memory_id: str = None,
                         trigger: str = "", relevance_score: float = 0.0):
        """Record a retrieval event."""
        event_id = f"retr_{uuid.uuid4().hex[:8]}"
        self.conn.execute(
            "INSERT INTO retrieval_events (event_id, dump_id, memory_id, trigger, relevance_score, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
            (event_id, dump_id, memory_id, trigger, relevance_score, time.time()),
        )
        self.conn.commit()

    def get_retrieval_events(self) -> List[Dict[str, Any]]:
        """Get all retrieval events."""
        rows = self.conn.execute("SELECT * FROM retrieval_events ORDER BY timestamp").fetchall()
        return [dict(r) for r in rows]

    # ── Compression Events ───────────────────────────────────────────────

    def record_compression_event(self, event_id: str, session_id: str, trigger: str,
                                  context_ratio: float, messages_compressed: List[str],
                                  protected: List[str], pins: List[Dict], risk_level: str,
                                  risk_reason: str):
        """Record a compression event."""
        self.conn.execute(
            "INSERT INTO compression_events (event_id, session_id, trigger, context_ratio, messages_compressed_json, protected_json, pins_json, risk_level, risk_reason, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (event_id, session_id, trigger, context_ratio,
             json.dumps(messages_compressed), json.dumps(protected),
             json.dumps(pins), risk_level, risk_reason, time.time()),
        )
        self.conn.commit()

    # ── Integrity Reports ────────────────────────────────────────────────

    def record_integrity_report(self, report_id: str, event_id: str, checked_pins: int,
                                 preserved: int, weakened: int, lost: int,
                                 violations: List[Dict]):
        """Record an integrity report."""
        self.conn.execute(
            "INSERT INTO integrity_reports (report_id, event_id, checked_pins, preserved_correctly, weakened, lost, violations_json, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (report_id, event_id, checked_pins, preserved, weakened, lost,
             json.dumps(violations), time.time()),
        )
        self.conn.commit()
