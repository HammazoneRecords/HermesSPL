"""
Tests for pin integrity checks, memory bank, data dump, select_context, and agent tools.
"""

import os
import pytest
import sqlite3
import tempfile
import time
from lane_a_context_engine.pin_extraction import PinType, PinCandidate
from lane_a_context_engine.integrity import IntegrityChecker, IntegrityReport
from lane_a_context_engine.store import ContextMemoryStore
from lane_a_context_engine.retrieval import ContextRetriever
from lane_a_context_engine.tools import ContextEngineTools


class TestIntegrityChecks:
    """Test post-compression pin integrity verification."""

    def setup_method(self):
        self.checker = IntegrityChecker()

    def test_all_pins_preserved(self):
        """When all pins survive, report should show no violations."""
        pins = [
            PinCandidate("pin_001", "Must preserve this.", PinType.PRESERVE_EXACT, "msg_001", "test"),
        ]
        summary = "The summary includes: Must preserve this."
        report = self.checker.check(pins, summary)
        assert report.preserved_correctly == 1
        assert report.lost == 0
        assert len(report.violations) == 0

    def test_exact_pin_paraphrased_is_violation(self):
        """Preserve_exact pin that was paraphrased should be flagged."""
        pins = [
            PinCandidate("pin_001", "The memory bank must be read-only to the model.", PinType.PRESERVE_EXACT, "msg_001", "test"),
        ]
        summary = "The summary says the memory bank should be read-only for the model."
        report = self.checker.check(pins, summary)
        assert report.weakened == 1
        assert len(report.violations) >= 1

    def test_pin_lost_entirely(self):
        """Pin not mentioned in summary at all should be flagged as lost."""
        pins = [
            PinCandidate("pin_001", "Critical constraint about the system.", PinType.PRESERVE_EXACT, "msg_001", "test"),
        ]
        summary = "The summary talks about something completely different."
        report = self.checker.check(pins, summary)
        assert report.lost == 1

    def test_meaning_preserved_through_rephrase(self):
        """Preserve_meaning pin can be rephrased as long as meaning survives."""
        pins = [
            PinCandidate("pin_002", "The app simulates context loss during compression.", PinType.PRESERVE_MEANING, "msg_002", "test"),
        ]
        summary = "We discussed how the app models context degradation during compression."
        report = self.checker.check(pins, summary)
        # Meaning is roughly preserved — should not be a hard violation
        assert report.lost == 0

    def test_relationship_omitted_is_violation(self):
        """Preserve_relationship pin missing from summary should be flagged."""
        pins = [
            PinCandidate("pin_003", "The data dump feeds into the memory bank.", PinType.PRESERVE_RELATIONSHIP, "msg_003", "test"),
        ]
        summary = "The data dump is mentioned but not its relationship to the memory bank."
        report = self.checker.check(pins, summary)
        assert report.weakened + report.lost >= 1


class TestMemoryBank:
    """Test memory bank storage and retrieval."""

    def setup_method(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        self.store = ContextMemoryStore(self.db_path)

    def teardown_method(self):
        self.store.close()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_store_memory_entry(self):
        """Memory bank should store entries with content and source."""
        self.store.add_memory(
            content="The memory bank must be read-only to the model.",
            source_pin_id="pin_001",
            source_message_id="msg_001",
            importance=0.9,
        )
        entries = self.store.get_all_memory()
        assert len(entries) == 1
        assert entries[0]["content"] == "The memory bank must be read-only to the model."
        assert entries[0]["readonly"] == 1

    def test_memory_is_readonly(self):
        """Memory bank entries should be read-only by default."""
        self.store.add_memory(content="Test fact", importance=0.8)
        entries = self.store.get_all_memory()
        assert entries[0]["readonly"] == 1

    def test_search_memory_by_keyword(self):
        """Should search memory bank by keyword."""
        self.store.add_memory(content="The memory bank must be read-only.", importance=0.9)
        self.store.add_memory(content="The data dump stores compressed-out info.", importance=0.7)
        results = self.store.search_memory("memory bank")
        assert len(results) >= 1

    def test_search_memory_by_entity(self):
        """Should search memory bank by entity/topic."""
        self.store.add_memory(content="SQLite is used for the memory bank.", importance=0.8)
        results = self.store.search_memory("SQLite")
        assert len(results) >= 1

    def test_promote_dump_to_memory(self):
        """Should be able to promote a data dump entry to memory bank."""
        dump_id = self.store.add_to_dump(
            raw_content="Low-priority detail about compression.",
            entities_json='["compression"]',
        )
        self.store.promote_dump_to_memory(dump_id, importance=0.6)
        memory = self.store.get_all_memory()
        assert len(memory) == 1
        assert "Low-priority detail" in memory[0]["content"]


class TestDataDump:
    """Test data dump archival and re-integration."""

    def setup_method(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        self.store = ContextMemoryStore(self.db_path)

    def teardown_method(self):
        self.store.close()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_archive_to_dump(self):
        """Data dump should store compressed-out information."""
        dump_id = self.store.add_to_dump(
            raw_content="Original message text here.",
            summary="Short summary of the content.",
            entities_json='["entity1", "entity2"]',
            retrieval_triggers_json='["keyword1", "keyword2"]',
            compression_event_id="comp_001",
        )
        entries = self.store.get_all_dump()
        assert len(entries) == 1
        assert entries[0]["dump_id"] == dump_id

    def test_search_dump_by_trigger(self):
        """Should search data dump by retrieval trigger."""
        self.store.add_to_dump(
            raw_content="Content about compression algorithms.",
            entities_json='["compression"]',
            retrieval_triggers_json='["compression", "algorithm"]',
        )
        results = self.store.search_dump("compression")
        assert len(results) >= 1

    def test_dump_preserves_raw_content(self):
        """Data dump should preserve original raw content."""
        raw = "This is the full original text that was compressed out."
        self.store.add_to_dump(raw_content=raw, summary="Compressed version.")
        entries = self.store.get_all_dump()
        assert entries[0]["raw_content"] == raw

    def test_track_retrieval_event(self):
        """Should track when a dump entry is retrieved."""
        dump_id = self.store.add_to_dump(raw_content="Test content.")
        self.store.record_retrieval(dump_id, trigger="test_trigger", relevance_score=0.85)
        events = self.store.get_retrieval_events()
        assert len(events) == 1
        assert events[0]["dump_id"] == dump_id


class TestSelectContext:
    """Test select_context() auto-injection of read-only memory."""

    def setup_method(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        self.store = ContextMemoryStore(self.db_path)
        self.retriever = ContextRetriever(self.store)

    def teardown_method(self):
        self.store.close()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_injects_relevant_memory(self):
        """select_context should inject relevant memory bank entries."""
        self.store.add_memory(content="The memory bank must be read-only.", importance=0.9)
        incoming = {"role": "user", "content": "Tell me about the memory bank."}
        result = self.retriever.select_context(
            request_messages=[incoming],
            conversation_messages=[],
            incoming_message=incoming,
            budget_tokens=10000,
        )
        # Result should contain injected memory context
        assert result is not None
        assert any("memory bank" in str(m.get("content", "")).lower() for m in result)

    def test_injects_as_readonly(self):
        """Injected memory should be marked as read-only context."""
        self.store.add_memory(content="Important fact.", importance=0.8)
        incoming = {"role": "user", "content": "What's important?"}
        result = self.retriever.select_context(
            request_messages=[incoming],
            conversation_messages=[],
            incoming_message=incoming,
            budget_tokens=10000,
        )
        # Injected messages should be clearly marked as retrieved/read-only
        assert any("retrieved" in str(m.get("content", "")).lower() or
                   "memory" in str(m.get("content", "")).lower() for m in result)

    def test_no_injection_when_no_match(self):
        """If nothing relevant in memory bank, should return None (no-op)."""
        self.store.add_memory(content="Fact about weather.", importance=0.5)
        incoming = {"role": "user", "content": "Tell me about quantum physics."}
        result = self.retriever.select_context(
            request_messages=[incoming],
            conversation_messages=[],
            incoming_message=incoming,
            budget_tokens=10000,
        )
        # No relevant match — should return None to leave request unchanged
        assert result is None

    def test_injects_dump_matches_too(self):
        """Should also retrieve from data dump if relevant."""
        self.store.add_to_dump(
            raw_content="The compression algorithm uses hierarchical summarization.",
            entities_json='["compression"]',
            retrieval_triggers_json='["compression", "algorithm"]',
        )
        incoming = {"role": "user", "content": "How does compression work?"}
        result = self.retriever.select_context(
            request_messages=[incoming],
            conversation_messages=[],
            incoming_message=incoming,
            budget_tokens=10000,
        )
        assert result is not None


class TestAgentTools:
    """Test agent-callable tools for pin/memory management."""

    def setup_method(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        self.store = ContextMemoryStore(self.db_path)
        self.tools = ContextEngineTools(self.store)

    def teardown_method(self):
        self.store.close()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_context_pin_tool(self):
        """context_pin tool should create a new pin."""
        result = self.tools.handle_tool_call("context_pin", {
            "content": "Must preserve this fact.",
            "pin_type": "preserve_exact",
            "reason": "User request",
        })
        assert result["ok"] == True
        assert "pin_id" in result

    def test_context_unpin_tool(self):
        """context_unpin tool should deactivate a pin."""
        pin_result = self.tools.handle_tool_call("context_pin", {
            "content": "Fact to unpin.",
            "pin_type": "preserve_meaning",
        })
        unpin_result = self.tools.handle_tool_call("context_unpin", {
            "pin_id": pin_result["pin_id"],
        })
        assert unpin_result["ok"] == True

    def test_context_search_memory_tool(self):
        """context_search_memory tool should search the memory bank."""
        self.store.add_memory(content="Memory bank fact about SQLite.", importance=0.8)
        result = self.tools.handle_tool_call("context_search_memory", {
            "query": "SQLite",
        })
        assert result["ok"] == True
        assert len(result["results"]) >= 1

    def test_context_search_dump_tool(self):
        """context_search_dump tool should search the data dump."""
        self.store.add_to_dump(
            raw_content="Detail about compression.",
            entities_json='["compression"]',
        )
        result = self.tools.handle_tool_call("context_search_dump", {
            "query": "compression",
        })
        assert result["ok"] == True
        assert len(result["results"]) >= 1

    def test_context_promote_tool(self):
        """context_promote tool should move dump entry to memory bank."""
        dump_id = self.store.add_to_dump(raw_content="Important detail.")
        result = self.tools.handle_tool_call("context_promote", {
            "dump_id": dump_id,
            "importance": 0.8,
        })
        assert result["ok"] == True
        memory = self.store.get_all_memory()
        assert len(memory) == 1

    def test_unknown_tool_returns_error(self):
        """Unknown tool name should return an error."""
        result = self.tools.handle_tool_call("nonexistent_tool", {})
        assert "error" in result

    def test_get_tool_schemas(self):
        """Should return schemas for all tools."""
        schemas = self.tools.get_tool_schemas()
        tool_names = [s["name"] for s in schemas]
        assert "context_pin" in tool_names
        assert "context_unpin" in tool_names
        assert "context_search_memory" in tool_names
        assert "context_search_dump" in tool_names
        assert "context_promote" in tool_names
