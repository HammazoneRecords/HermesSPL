"""Compression plan generator — pre-compression inspection."""

import uuid
from dataclasses import dataclass, field
from typing import List, Optional

from lane_a_context_engine.pin_extraction import PinCandidate, PinExtractor, PinType


@dataclass
class CompressionPlan:
    """Plan for a single compression event."""
    compression_event_id: str
    session_id: str
    trigger: str  # "automatic" or "manual"
    context_ratio: float
    messages_to_compress: List[str] = field(default_factory=list)
    protected_message_ids: List[str] = field(default_factory=list)
    pins: List[PinCandidate] = field(default_factory=list)
    risk_level: str = "low"
    risk_reason: str = ""


class CompressionPlanGenerator:
    """Generates compression plans by inspecting messages for pins."""

    def __init__(self, extractor: Optional[PinExtractor] = None):
        self.extractor = extractor or PinExtractor()

    def generate_plan(
        self,
        messages: List[dict],
        context_ratio: float,
        session_id: str = "",
        trigger: str = "automatic",
        protect_first_n: int = 3,
        protect_last_n: int = 6,
    ) -> CompressionPlan:
        """Generate a compression plan from messages."""
        # Extract all pin candidates
        pins = self.extractor.extract_from_messages(messages)

        # Determine which messages are in the compression zone
        msg_ids = [m.get("msg_id", f"msg_{i:04d}") for i, m in enumerate(messages)]

        # Protected: head + tail
        protected = set()
        for i in range(min(protect_first_n, len(msg_ids))):
            protected.add(msg_ids[i])
        for i in range(max(len(msg_ids) - protect_last_n, protect_first_n), len(msg_ids)):
            protected.add(msg_ids[i])

        # Messages to compress = middle (not protected)
        to_compress = [mid for mid in msg_ids if mid not in protected]
        
        # If nothing to compress (small conversation), still generate plan
        # but mark that compression may not be needed yet

        # Assign destinations to pins
        for pin in pins:
            if pin.pin_type == PinType.PRESERVE_EXACT:
                pin.destination = "memory_bank"
            elif pin.pin_type == PinType.NEVER_COMPRESS_AWAY:
                pin.destination = "memory_bank"
            elif pin.pin_type == PinType.ARCHIVE_BUT_RETRIEVE:
                pin.destination = "data_dump"
            else:
                pin.destination = "summary"

        # Compute risk level
        risk_level = self._compute_risk(pins, to_compress)

        return CompressionPlan(
            compression_event_id=f"comp_{uuid.uuid4().hex[:8]}",
            session_id=session_id,
            trigger=trigger,
            context_ratio=context_ratio,
            messages_to_compress=list(to_compress),
            protected_message_ids=list(protected),
            pins=pins,
            risk_level=risk_level,
            risk_reason=self._risk_reason(pins, to_compress),
        )

    def _compute_risk(self, pins: List[PinCandidate], to_compress: List[str]) -> str:
        """Compute risk level based on what's being compressed."""
        if not pins:
            return "low"
        exact_pins = [p for p in pins if p.pin_type in (PinType.PRESERVE_EXACT, PinType.NEVER_COMPRESS_AWAY)]
        if len(exact_pins) >= 3:
            return "high"
        elif len(exact_pins) >= 1:
            return "medium"
        return "low"

    def _risk_reason(self, pins: List[PinCandidate], to_compress: List[str]) -> str:
        """Generate human-readable risk reason."""
        if not pins:
            return "No pinned items in compression zone."
        return f"{len(pins)} pin(s) in compression zone, {len(to_compress)} message(s) to compress."
