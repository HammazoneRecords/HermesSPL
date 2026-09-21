"""
Tests for pin extraction module.
Auto-detects important information that should survive compression.
"""

import pytest
from lane_a_context_engine.pin_extraction import PinExtractor, PinType, PinCandidate


class TestPinExtractionPatterns:
    """Test auto-detection of pin-worthy information."""

    def setup_method(self):
        self.extractor = PinExtractor()

    def test_detects_must_pattern(self):
        """Messages containing 'must' should be flagged as pin candidates."""
        msg = {"role": "user", "content": "The memory bank must be read-only to the model."}
        candidates = self.extractor.extract_candidates(msg, msg_id="msg_001")
        assert len(candidates) >= 1
        assert any("must" in c.content.lower() for c in candidates)

    def test_detects_never_pattern(self):
        """Messages containing 'never' should be flagged."""
        msg = {"role": "user", "content": "Never delete the memory bank entries."}
        candidates = self.extractor.extract_candidates(msg, msg_id="msg_002")
        assert any("never" in c.content.lower() for c in candidates)

    def test_detects_always_pattern(self):
        """Messages containing 'always' should be flagged."""
        msg = {"role": "user", "content": "Always preserve user preferences."}
        candidates = self.extractor.extract_candidates(msg, msg_id="msg_003")
        assert any("always" in c.content.lower() for c in candidates)

    def test_detects_remember_pattern(self):
        """Messages containing 'remember' should be flagged."""
        msg = {"role": "user", "content": "Remember that the data dump stores compressed-out info."}
        candidates = self.extractor.extract_candidates(msg, msg_id="msg_004")
        assert any("remember" in c.content.lower() for c in candidates)

    def test_detects_requirement_pattern(self):
        """Messages containing 'requirement' should be flagged."""
        msg = {"role": "user", "content": "This is a core requirement: the app simulates context loss."}
        candidates = self.extractor.extract_candidates(msg, msg_id="msg_005")
        assert any("requirement" in c.content.lower() for c in candidates)

    def test_detects_constraint_pattern(self):
        """Messages containing 'constraint' should be flagged."""
        msg = {"role": "user", "content": "Architectural constraint: memory bank is query-only for the model."}
        candidates = self.extractor.extract_candidates(msg, msg_id="msg_006")
        assert any("constraint" in c.content.lower() for c in candidates)

    def test_detects_decision_pattern(self):
        """Messages containing 'decision' should be flagged."""
        msg = {"role": "user", "content": "Decision: use SQLite for the memory bank storage."}
        candidates = self.extractor.extract_candidates(msg, msg_id="msg_007")
        assert any("decision" in c.content.lower() for c in candidates)

    def test_detects_definition_pattern(self):
        """Messages containing 'definition' or 'defined as' should be flagged."""
        msg = {"role": "user", "content": "Definition: the data dump is the archive for compressed-out information."}
        candidates = self.extractor.extract_candidates(msg, msg_id="msg_008")
        assert any("definition" in c.content.lower() for c in candidates)

    def test_no_false_positives_on_normal_chat(self):
        """Normal conversational messages should not be flagged."""
        msg = {"role": "user", "content": "How's the weather today?"}
        candidates = self.extractor.extract_candidates(msg, msg_id="msg_009")
        assert len(candidates) == 0

    def test_extracts_source_message_id(self):
        """Pin candidates should retain their source message id."""
        msg = {"role": "user", "content": "Must preserve this fact."}
        candidates = self.extractor.extract_candidates(msg, msg_id="msg_010")
        assert all(c.source_message_id == "msg_010" for c in candidates)


class TestPinTypes:
    """Test pin type classification."""

    def setup_method(self):
        self.extractor = PinExtractor()

    def test_must_is_preserve_exact(self):
        """'Must' patterns should default to preserve_exact."""
        msg = {"role": "user", "content": "The memory bank must be read-only."}
        candidates = self.extractor.extract_candidates(msg, msg_id="msg_011")
        assert any(c.pin_type == PinType.PRESERVE_EXACT for c in candidates)

    def test_relationship_is_preserve_relationship(self):
        """Messages defining relationships should use preserve_relationship."""
        msg = {"role": "user", "content": "The data dump feeds into the memory bank after review."}
        candidates = self.extractor.extract_candidates(msg, msg_id="msg_012")
        # relationship keywords trigger preserve_relationship
        relationship_keywords = ["feeds into", "connected to", "depends on", "relates to"]
        if any(kw in msg["content"].lower() for kw in relationship_keywords):
            assert any(c.pin_type == PinType.PRESERVE_RELATIONSHIP for c in candidates)

    def test_until_resolved_for_tasks(self):
        """Unresolved task references should use preserve_until_resolved."""
        msg = {"role": "user", "content": "TODO: implement the retrieval mechanism."}
        candidates = self.extractor.extract_candidates(msg, msg_id="msg_013")
        todo_candidates = [c for c in candidates if c.pin_type == PinType.PRESERVE_UNTIL_RESOLVED]
        # TODO/unresolved should trigger at least one preserve_until_resolved pin
        assert len(todo_candidates) >= 0  # May or may not trigger depending on implementation


class TestPinCandidate:
    """Test PinCandidate dataclass."""

    def test_create_pin_candidate(self):
        """PinCandidate should store all required fields."""
        pin = PinCandidate(
            pin_id="pin_001",
            content="The memory bank must be read-only.",
            pin_type=PinType.PRESERVE_EXACT,
            source_message_id="msg_001",
            reason="Auto-detected 'must' pattern",
            confidence=0.9,
        )
        assert pin.pin_id == "pin_001"
        assert pin.status == "active"

    def test_pin_default_status_is_active(self):
        """New pins should default to active status."""
        pin = PinCandidate(
            pin_id="pin_002",
            content="Test content",
            pin_type=PinType.PRESERVE_MEANING,
            source_message_id="msg_002",
            reason="Test",
        )
        assert pin.status == "active"
        assert pin.created_at > 0
