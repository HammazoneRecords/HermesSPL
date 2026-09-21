"""
Tests for pin types and compression plan generation.
"""

import pytest
from lane_a_context_engine.pin_extraction import PinType, PinCandidate
from lane_a_context_engine.compression_plan import CompressionPlan, CompressionPlanGenerator


class TestCompressionPlanGeneration:
    """Test pre-compression inspection and plan generation."""

    def setup_method(self):
        self.generator = CompressionPlanGenerator()

    def test_generates_plan_with_pins(self):
        """Compression plan should include detected pins."""
        messages = [
            {"role": "user", "content": "The memory bank must be read-only to the model.", "msg_id": "msg_001"},
            {"role": "assistant", "content": "Understood.", "msg_id": "msg_002"},
            {"role": "user", "content": "How's the weather?", "msg_id": "msg_003"},
        ]
        plan = self.generator.generate_plan(messages, context_ratio=0.51)
        assert plan.compression_event_id is not None
        assert len(plan.pins) > 0

    def test_plan_identifies_messages_to_compress(self):
        """Plan which messages are in the compression zone (middle, not head/tail)."""
        messages = [
            {"role": "user", "content": "The memory bank must be read-only.", "msg_id": "msg_001"},
            {"role": "assistant", "content": "Got it.", "msg_id": "msg_002"},
            {"role": "user", "content": "Also, the data dump stores compressed-out info.", "msg_id": "msg_003"},
            {"role": "assistant", "content": "Noted.", "msg_id": "msg_004"},
            {"role": "user", "content": "What's next?", "msg_id": "msg_005"},
        ]
        plan = self.generator.generate_plan(messages, context_ratio=0.51, protect_first_n=1, protect_last_n=1)
        # Middle messages should be in compression zone
        assert len(plan.messages_to_compress) > 0

    def test_plan_preserves_head_and_tail(self):
        """Plan should mark head and tail messages as protected."""
        messages = [
            {"role": "user", "content": "First message with must pattern.", "msg_id": "msg_001"},
            {"role": "assistant", "content": "Response.", "msg_id": "msg_002"},
            {"role": "user", "content": "Middle message.", "msg_id": "msg_003"},
            {"role": "assistant", "content": "Response.", "msg_id": "msg_004"},
            {"role": "user", "content": "Last message.", "msg_id": "msg_005"},
        ]
        plan = self.generator.generate_plan(messages, context_ratio=0.51, protect_first_n=1, protect_last_n=1)
        protected_ids = plan.protected_message_ids
        assert "msg_001" in protected_ids  # head
        assert "msg_005" in protected_ids  # tail

    def test_plan_assigns_destinations(self):
        """Plan should assign each pin a destination (summary, memory_bank, data_dump)."""
        messages = [
            {"role": "user", "content": "Must preserve this exactly: the memory bank is read-only.", "msg_id": "msg_001"},
            {"role": "assistant", "content": "OK.", "msg_id": "msg_002"},
            {"role": "user", "content": "Random chat.", "msg_id": "msg_003"},
        ]
        plan = self.generator.generate_plan(messages, context_ratio=0.51)
        for pin in plan.pins:
            assert pin.destination in ("summary", "memory_bank", "data_dump")

    def test_plan_risk_level(self):
        """Plan should compute a risk level based on what's being compressed."""
        messages = [
            {"role": "user", "content": "Must do this. Never do that. Always remember.", "msg_id": "msg_001"},
            {"role": "assistant", "content": "OK.", "msg_id": "msg_002"},
            {"role": "user", "content": "More content.", "msg_id": "msg_003"},
        ]
        plan = self.generator.generate_plan(messages, context_ratio=0.51)
        assert plan.risk_level in ("low", "medium", "high")


class TestPinTypes:
    """Test all six pin types."""

    def test_preserve_exact_type(self):
        pin = PinCandidate(
            pin_id="pin_001",
            content="Exact text to preserve",
            pin_type=PinType.PRESERVE_EXACT,
            source_message_id="msg_001",
            reason="Test",
        )
        assert pin.pin_type == PinType.PRESERVE_EXACT

    def test_preserve_meaning_type(self):
        pin = PinCandidate(
            pin_id="pin_002",
            content="Meaning to preserve",
            pin_type=PinType.PRESERVE_MEANING,
            source_message_id="msg_002",
            reason="Test",
        )
        assert pin.pin_type == PinType.PRESERVE_MEANING

    def test_preserve_relationship_type(self):
        pin = PinCandidate(
            pin_id="pin_003",
            content="A depends on B",
            pin_type=PinType.PRESERVE_RELATIONSHIP,
            source_message_id="msg_003",
            reason="Test",
        )
        assert pin.pin_type == PinType.PRESERVE_RELATIONSHIP

    def test_preserve_until_resolved_type(self):
        pin = PinCandidate(
            pin_id="pin_004",
            content="TODO: implement feature X",
            pin_type=PinType.PRESERVE_UNTIL_RESOLVED,
            source_message_id="msg_004",
            reason="Test",
        )
        assert pin.pin_type == PinType.PRESERVE_UNTIL_RESOLVED

    def test_never_compress_away_type(self):
        pin = PinCandidate(
            pin_id="pin_005",
            content="Core identity fact",
            pin_type=PinType.NEVER_COMPRESS_AWAY,
            source_message_id="msg_005",
            reason="Test",
        )
        assert pin.pin_type == PinType.NEVER_COMPRESS_AWAY

    def test_archive_but_retrieve_type(self):
        pin = PinCandidate(
            pin_id="pin_006",
            content="Low-priority detail",
            pin_type=PinType.ARCHIVE_BUT_RETRIEVE,
            source_message_id="msg_006",
            reason="Test",
        )
        assert pin.pin_type == PinType.ARCHIVE_BUT_RETRIEVE
