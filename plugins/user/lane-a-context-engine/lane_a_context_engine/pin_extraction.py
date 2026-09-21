"""Pin extraction module — auto-detects important information for compression."""

import re
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class PinType(Enum):
    """Types of compression pins."""
    PRESERVE_EXACT = "preserve_exact"
    PRESERVE_MEANING = "preserve_meaning"
    PRESERVE_RELATIONSHIP = "preserve_relationship"
    PRESERVE_UNTIL_RESOLVED = "preserve_until_resolved"
    NEVER_COMPRESS_AWAY = "never_compress_away"
    ARCHIVE_BUT_RETRIEVE = "archive_but_retrieve"


# Patterns that indicate pin-worthy content
PIN_PATTERNS = [
    (r'\bmust\b', PinType.PRESERVE_EXACT, "Auto-detected 'must' pattern"),
    (r'\bnever\b', PinType.PRESERVE_EXACT, "Auto-detected 'never' pattern"),
    (r'\balways\b', PinType.PRESERVE_EXACT, "Auto-detected 'always' pattern"),
    (r'\bremember\b', PinType.PRESERVE_EXACT, "Auto-detected 'remember' pattern"),
    (r'\brequirement\b', PinType.PRESERVE_EXACT, "Auto-detected 'requirement' pattern"),
    (r'\bconstraint\b', PinType.PRESERVE_EXACT, "Auto-detected 'constraint' pattern"),
    (r'\bdecision\b', PinType.PRESERVE_EXACT, "Auto-detected 'decision' pattern"),
    (r'\bdefinition\b', PinType.PRESERVE_EXACT, "Auto-detected 'definition' pattern"),
    (r'\bdefined as\b', PinType.PRESERVE_EXACT, "Auto-detected 'defined as' pattern"),
    (r'\bTODO\b', PinType.PRESERVE_UNTIL_RESOLVED, "Auto-detected TODO"),
    (r'\bunresolved\b', PinType.PRESERVE_UNTIL_RESOLVED, "Auto-detected unresolved item"),
    (r'\bfeeds into\b', PinType.PRESERVE_RELATIONSHIP, "Auto-detected relationship"),
    (r'\bconnected to\b', PinType.PRESERVE_RELATIONSHIP, "Auto-detected relationship"),
    (r'\bdepends on\b', PinType.PRESERVE_RELATIONSHIP, "Auto-detected relationship"),
    (r'\brelates to\b', PinType.PRESERVE_RELATIONSHIP, "Auto-detected relationship"),
]


@dataclass
class PinCandidate:
    """A piece of information that should survive compression."""
    pin_id: str
    content: str
    pin_type: PinType
    source_message_id: str
    reason: str
    confidence: float = 0.8
    status: str = "active"
    created_at: float = field(default_factory=time.time)
    destination: str = "summary"  # summary, memory_bank, data_dump


class PinExtractor:
    """Extracts pin candidates from messages."""

    def __init__(self, custom_patterns=None):
        self.patterns = PIN_PATTERNS + (custom_patterns or [])

    def extract_candidates(self, message: dict, msg_id: str) -> List[PinCandidate]:
        """Extract pin candidates from a single message."""
        content = message.get("content", "")
        if not content:
            return []

        candidates = []
        for pattern, pin_type, reason in self.patterns:
            if re.search(pattern, content, re.IGNORECASE):
                pin = PinCandidate(
                    pin_id=f"pin_{uuid.uuid4().hex[:8]}",
                    content=content,
                    pin_type=pin_type,
                    source_message_id=msg_id,
                    reason=reason,
                )
                candidates.append(pin)

        return candidates

    def extract_from_messages(self, messages: List[dict]) -> List[PinCandidate]:
        """Extract pin candidates from a list of messages."""
        all_candidates = []
        for i, msg in enumerate(messages):
            msg_id = msg.get("msg_id", f"msg_{i:04d}")
            candidates = self.extract_candidates(msg, msg_id)
            all_candidates.extend(candidates)
        return all_candidates
