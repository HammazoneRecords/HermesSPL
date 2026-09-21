"""
Lane A Context Engine Plugin v2

Pin-aware compression with:
1. Transient notifications at configurable thresholds
2. Automatic summary persistence to SQLite DB
3. Pin extraction (auto-detect important info)
4. Memory bank (read-only auto-retrieved context)
5. Data dump (archived compressed-out info)
6. Context-aware retrieval via select_context()
7. Agent-callable tools (context_pin, context_unpin, etc.)

Usage:
    context:
      engine: lane-a-engine
      lane_a:
        notifications:
          enabled: true
          thresholds: [0.50, 0.60]
          style: transient
        db:
          enabled: true
          path: "~/.hermes/state.db"
          table: lane_a_summaries
        memory:
          enabled: true
          path: "~/.hermes/lane_a_memory.db"
"""

import json
import logging
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from agent.context_compressor import ContextCompressor
from agent.context_engine import ContextEngine

from lane_a_context_engine.pin_extraction import PinExtractor, PinType
from lane_a_context_engine.compression_plan import CompressionPlanGenerator
from lane_a_context_engine.integrity import IntegrityChecker
from lane_a_context_engine.store import ContextMemoryStore
from lane_a_context_engine.retrieval import ContextRetriever
from lane_a_context_engine.tools import ContextEngineTools
from lane_a_context_engine.notifications import NotificationChecker

logger = logging.getLogger(__name__)

LANE_A_DEFAULTS = {
    "notifications": {
        "enabled": True,
        "thresholds": [0.50, 0.60],
        "style": "transient",
    },
    "db": {
        "enabled": True,
        "path": "~/.hermes/state.db",
        "table": "lane_a_summaries",
    },
    "memory": {
        "enabled": True,
        "path": "~/.hermes/lane_a_memory.db",
    },
}


class LaneAContextEngine(ContextEngine):
    """Lane A context engine with pin-aware compression, memory bank, and retrieval."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__()
        self.config = config or {}
        self.lane_a_config = self.config.get("lane_a", LANE_A_DEFAULTS)
        self.notifications_cfg = self.lane_a_config.get("notifications", LANE_A_DEFAULTS["notifications"])
        self.db_cfg = self.lane_a_config.get("db", LANE_A_DEFAULTS["db"])
        self.memory_cfg = self.lane_a_config.get("memory", LANE_A_DEFAULTS["memory"])

        # Subsystems
        self._compressor = ContextCompressor()
        self._extractor = PinExtractor()
        self._plan_generator = CompressionPlanGenerator(self._extractor)
        self._integrity_checker = IntegrityChecker()
        self._notification_checker = NotificationChecker(self.notifications_cfg.get("thresholds", [0.5, 0.6]))

        # Memory store (lazy init)
        self._store = None
        self._retriever = None
        self._tools = None

        # Track pins for current session
        self._session_pins = []

    @property
    def name(self) -> str:
        return "lane-a-engine"

    def _init_store(self):
        """Lazy-initialize the memory store."""
        if self._store is None and self.memory_cfg.get("enabled", True):
            db_path = str(Path(self.memory_cfg.get("path", "~/.hermes/lane_a_memory.db")).expanduser())
            self._store = ContextMemoryStore(db_path)
            self._retriever = ContextRetriever(self._store)
            self._tools = ContextEngineTools(self._store)

    def update_from_response(self, usage: Dict[str, Any]) -> None:
        self._compressor.update_from_response(usage)

    def should_compress(self, prompt_tokens: int = None) -> bool:
        tokens = prompt_tokens or self._compressor.last_prompt_tokens
        context_length = self._compressor.context_length
        if context_length > 0:
            ratio = tokens / context_length
            notifications = self._notification_checker.check(ratio, tokens, context_length)
            for n in notifications:
                print(f"📊 {n}")
        return self._compressor.should_compress(prompt_tokens)

    def compress(self, messages, current_tokens=None, focus_topic=None, force=False, memory_context=""):
        """Pin-aware compression with integrity checks."""
        self._init_store()

        # Generate compression plan
        plan = self._plan_generator.generate_plan(
            messages=messages,
            context_ratio=(current_tokens / self._compressor.context_length) if self._compressor.context_length > 0 else 0,
            trigger="automatic" if not force else "manual",
        )

        # Store pins in memory bank
        if self._store:
            for pin in plan.pins:
                if pin.pin_type in (PinType.PRESERVE_EXACT, PinType.NEVER_COMPRESS_AWAY):
                    self._store.add_memory(
                        content=pin.content,
                        source_pin_id=pin.pin_id,
                        source_message_id=pin.source_message_id,
                        importance=0.9 if pin.pin_type == PinType.PRESERVE_EXACT else 0.7,
                    )
                elif pin.pin_type == PinType.ARCHIVE_BUT_RETRIEVE:
                    self._store.add_to_dump(
                        raw_content=pin.content,
                        entities_json=json.dumps([]),
                        retrieval_triggers_json=json.dumps([]),
                    )

        # Perform actual compression using built-in compressor
        result = self._compressor.compress(messages, current_tokens, focus_topic, force, memory_context)

        # Run integrity check
        if plan.pins:
            summary_text = result[0].get("content", "") if result else ""
            report = self._integrity_checker.check(plan.pins, summary_text, plan.compression_event_id)
            if report.violations:
                for v in report.violations:
                    logger.warning(f"Pin integrity: {v.issue}")

        # Store summary to DB
        self._store_summary_to_db(result)

        return result

    def select_context(self, request_messages, *, conversation_messages=None, incoming_message=None, budget_tokens=0):
        """Auto-inject read-only memory bank entries."""
        self._init_store()
        if self._retriever:
            return self._retriever.select_context(
                request_messages=request_messages,
                conversation_messages=conversation_messages or [],
                incoming_message=incoming_message,
                budget_tokens=budget_tokens,
            )
        return None

    def on_turn_complete(self, messages, usage=None, **kwargs):
        """Observe completed turn — extract and index any new pins."""
        self._init_store()
        if self._store:
            for i, msg in enumerate(messages):
                msg_id = msg.get("msg_id", f"msg_{i:04d}")
                candidates = self._extractor.extract_candidates(msg, msg_id)
                for pin in candidates:
                    self._store.add_pin(
                        pin_id=pin.pin_id,
                        content=pin.content,
                        pin_type=pin.pin_type.value,
                        source_message_id=pin.source_message_id,
                        reason=pin.reason,
                    )

    def get_tool_schemas(self):
        """Expose pin/memory tools to the agent."""
        self._init_store()
        if self._tools:
            return self._tools.get_tool_schemas()
        return []

    def handle_tool_call(self, name, args, **kwargs):
        """Handle tool calls for pin/memory management."""
        self._init_store()
        if self._tools:
            return self._tools.handle_tool_call(name, args)
        return json.dumps({"error": "Tools not initialized"})

    def _store_summary_to_db(self, summary_messages):
        """Store compression summary to SQLite."""
        if not self.db_cfg.get("enabled", True):
            return
        db_path = str(Path(self.db_cfg.get("path", "~/.hermes/state.db")).expanduser())
        table = self.db_cfg.get("table", "lane_a_summaries")

        summary_text = summary_messages[0].get("content", "") if summary_messages else ""
        last_prompt = self._compressor.last_prompt_tokens if self._compressor.last_prompt_tokens > 0 else 0
        ratio = last_prompt / self._compressor.context_length if self._compressor.context_length > 0 else 0.0

        try:
            conn = sqlite3.connect(db_path)
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    compression_count INTEGER NOT NULL,
                    summary TEXT NOT NULL,
                    context_ratio REAL,
                    prompt_tokens INTEGER,
                    context_length INTEGER,
                    timestamp REAL NOT NULL,
                    lane TEXT DEFAULT 'A',
                    metadata TEXT
                )
            """)
            conn.execute(
                f"INSERT INTO {table} (session_id, compression_count, summary, context_ratio, prompt_tokens, context_length, timestamp, lane, metadata) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (None, self._compressor.compression_count, summary_text, ratio, last_prompt, self._compressor.context_length, time.time(), "A", json.dumps({"source": "lane-a-context-engine-v2"})),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.warning(f"Failed to store Lane A summary: {e}")

    def on_session_start(self, session_id, **kwargs):
        self._notification_checker.reset()
        self._session_pins.clear()

    def on_session_end(self, session_id, messages):
        self._notification_checker.reset()
        if self._store:
            self._store.close()

    def on_session_reset(self):
        self._compressor.on_session_reset()
        self._notification_checker.reset()
        self._session_pins.clear()

    def get_status(self):
        return self._compressor.get_status()


def register_context_engine(config=None):
    """Entry point for plugin registration."""
    return LaneAContextEngine(config)
