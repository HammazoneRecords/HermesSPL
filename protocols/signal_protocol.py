"""Explicit Signal Protocol state machine with gated outputs and receipts."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import count
from typing import Any, Dict, FrozenSet, Mapping


class SignalProtocolError(ValueError):
    """Base error for malformed protocol operations."""


class AmbiguousStateError(SignalProtocolError):
    """Raised when a state is not exactly one of the five defined states."""


class InvalidTransitionError(SignalProtocolError):
    """Raised when a requested state transition is not permitted."""


class OutputPermissionError(SignalProtocolError):
    """Raised when the current state cannot emit the requested output."""


@dataclass(frozen=True)
class SignalState:
    code: str

    def __post_init__(self) -> None:
        if self.code not in SignalProtocol.STATES:
            raise AmbiguousStateError(f"unknown or ambiguous state: {self.code!r}")


class SignalProtocol:
    """Finite state protocol: 000 → 001 → 010 → 100 → 111."""

    STATES = frozenset(("000", "001", "010", "100", "111"))
    TRANSITIONS = {
        "000": frozenset(("000", "001")),
        "001": frozenset(("001", "010")),
        "010": frozenset(("010", "100")),
        "100": frozenset(("100", "111")),
        "111": frozenset(("111",)),
    }
    OUTPUT_PERMISSIONS = {
        "000": frozenset(),
        "001": frozenset(("status",)),
        "010": frozenset(("status", "diagnostic")),
        "100": frozenset(("status", "diagnostic", "response")),
        "111": frozenset(("status", "diagnostic", "response", "external")),
    }
    _receipt_ids = count(1)

    def __init__(self, initial_state: str = "000") -> None:
        self._state = self._validate_state(initial_state)
        self._last_receipt: Dict[str, Any] | None = None

    @classmethod
    def _validate_state(cls, state: str) -> SignalState:
        if not isinstance(state, str) or state not in cls.STATES:
            raise AmbiguousStateError(f"unknown or ambiguous state: {state!r}")
        return SignalState(state)

    @property
    def state(self) -> SignalState:
        return self._state

    @property
    def last_receipt(self) -> Mapping[str, Any] | None:
        return self._last_receipt

    def _receipt(self, event: str, accepted: bool, **fields: Any) -> Dict[str, Any]:
        receipt = {
            "receipt_id": f"signal-{next(self._receipt_ids):06d}",
            "protocol": "signal",
            "event": event,
            "accepted": accepted,
            "state": self._state.code,
            **fields,
        }
        self._last_receipt = receipt
        return receipt

    def transition(self, target: str) -> Dict[str, Any]:
        try:
            target_state = self._validate_state(target)
        except AmbiguousStateError as exc:
            self._receipt("transition_rejected", False, requested_state=target, reason=str(exc))
            raise
        if target_state.code not in self.TRANSITIONS[self._state.code]:
            receipt = self._receipt(
                "transition_rejected", False, from_state=self._state.code,
                requested_state=target_state.code, reason="invalid transition",
            )
            raise InvalidTransitionError(receipt["reason"])
        previous = self._state.code
        self._state = target_state
        return self._receipt("transition", True, from_state=previous, to_state=target_state.code)

    def can_output(self, output_kind: str) -> bool:
        return output_kind in self.OUTPUT_PERMISSIONS[self._state.code]

    def gate_output(self, output_kind: str, payload: Any) -> Dict[str, Any]:
        if not isinstance(output_kind, str) or not self.can_output(output_kind):
            receipt = self._receipt(
                "output_rejected", False, output_kind=output_kind,
                reason="output not permitted in current state",
            )
            raise OutputPermissionError(receipt["reason"])
        return self._receipt("output_allowed", True, output_kind=output_kind, payload=payload)
