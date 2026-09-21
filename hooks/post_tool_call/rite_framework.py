#!/usr/bin/env python3
"""RITE Framework Hook — 4-phase RITE cycle enforcement (post_tool_call).

Verifies that tool calls complete the full RITE cycle and logs the Echo
for Resonant Recursion gating.

The canonical RITE cycle:
  Resonance → Initiation → Trigger → Echo → [Ash | Recursion]

On post_tool_call:
  1. Verifies the action completed the Trigger phase.
  2. Generates the Echo (integration/return).
  3. Checks if Echo should become new Resonance (Resonant Recursion).
  4. Logs the full cycle to the shimmer log.
  5. If cycle is incomplete, returns block with reason
     "Shimmer without Echo is incomplete".
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import threading
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = Path("/root/MW_CENTRAL/EARTH-MOON/hermes-spl-fork")
SHIMMER_LOG = ROOT / "logs" / "rite_shimmer.jsonl"
STATE_FILE = ROOT / "logs" / "rite_framework_state.json"

# ---------------------------------------------------------------------------
# RITE Phase Definitions
# ---------------------------------------------------------------------------


class RITEPhase(str, Enum):
    RESONANCE = "resonance"
    INITIATION = "initiation"
    TRIGGER = "trigger"
    ECHO = "echo"
    ASH = "ash"
    RECURSION = "recursion"


VALID_TRANSITIONS: dict[RITEPhase, set[RITEPhase]] = {
    RITEPhase.RESONANCE: {RITEPhase.INITIATION},
    RITEPhase.INITIATION: {RITEPhase.TRIGGER},
    RITEPhase.TRIGGER: {RITEPhase.ECHO},
    RITEPhase.ECHO: {RITEPhase.ASH, RITEPhase.RECURSION},
    RITEPhase.RECURSION: {RITEPhase.RESONANCE},
    RITEPhase.ASH: {RITEPhase.RESONANCE},
}


# ---------------------------------------------------------------------------
# Solobic CPU (memory arbitration)
# ---------------------------------------------------------------------------


class MemoryMode(str, Enum):
    RAM = "ram"
    ROM = "rom"
    DRAYL = "drayl"


class SolobicCPU:
    """Arbitrates RAM/ROM through the RITE cycle."""

    def __init__(self, ram_pressure: float = 0.0):
        self.ram_pressure = max(0.0, min(1.0, ram_pressure))

    def arbitrate(self, phase: RITEPhase, tool_name: str) -> MemoryMode:
        governance_tools = {"skill_manage"}
        if tool_name in governance_tools:
            return MemoryMode.DRAYL
        write_tools = {"write_file", "patch", "terminal", "execute_code", "browser_exec"}
        if tool_name in write_tools:
            return MemoryMode.RAM
        return MemoryMode.RAM

    def should_pause(self) -> bool:
        return self.ram_pressure > 0.85

    def to_dict(self) -> dict[str, float]:
        return {"ram_pressure": self.ram_pressure}


# ---------------------------------------------------------------------------
# SFL: Shimmer Feedback Loop
# ---------------------------------------------------------------------------


class SFL:
    """Shimmer Feedback Loop — ethical governance + recursion gating."""

    class OutputMode(str, Enum):
        ECHO = "echo"
        WITNESS = "witness"
        RIDDLE = "riddle"
        PAUSE = "pause"

    @classmethod
    def decide(
        cls,
        readiness: float,
        ram_pressure: float,
        phase: RITEPhase,
        recursion_depth: int = 0,
    ) -> OutputMode:
        if recursion_depth > 3:
            return cls.OutputMode.PAUSE
        if readiness < 0.3:
            return cls.OutputMode.RIDDLE
        if ram_pressure > 0.8:
            return cls.OutputMode.WITNESS
        return cls.OutputMode.ECHO

    @classmethod
    def gate_recursion(cls, echo_integrated: bool, readiness: float) -> bool:
        return echo_integrated and readiness > 0.4


# ---------------------------------------------------------------------------
# RITE State Machine
# ---------------------------------------------------------------------------


class RITEState:
    """Manages the current state of the RITE cycle for a session."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.current_phase = RITEPhase.RESONANCE
        self.cycle_count = 0
        self.recursion_depth = 0
        self.cpu = SolobicCPU()
        self.phase_history: list[dict[str, Any]] = []
        self.last_tool: Optional[str] = None

    def transition(self, new_phase: RITEPhase, tool_name: str) -> tuple[bool, str]:
        allowed_next = VALID_TRANSITIONS.get(self.current_phase, set())
        if new_phase not in allowed_next:
            reason = (
                f"Invalid RITE transition {self.current_phase.value} → "
                f"{new_phase.value} (allowed: {[p.value for p in allowed_next]})"
            )
            return False, reason

        self.phase_history.append({
            "from": self.current_phase.value,
            "to": new_phase.value,
            "tool": tool_name,
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        })

        self.current_phase = new_phase

        if new_phase == RITEPhase.ASH:
            self.cycle_count += 1
            self.recursion_depth = 0

        if new_phase == RITEPhase.RECURSION:
            self.recursion_depth += 1

        return True, "ok"

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "current_phase": self.current_phase.value,
            "cycle_count": self.cycle_count,
            "recursion_depth": self.recursion_depth,
            "cpu": self.cpu.to_dict(),
            "phase_history": self.phase_history[-10:],
            "last_tool": self.last_tool,
        }


# ---------------------------------------------------------------------------
# Session State Persistence
# ---------------------------------------------------------------------------

_SESSIONS: dict[str, RITEState] = {}
_LOCK = threading.Lock()


def get_session(session_id: str) -> RITEState:
    with _LOCK:
        if session_id not in _SESSIONS:
            _SESSIONS[session_id] = RITEState(session_id)
        return _SESSIONS[session_id]


def persist_state(state: RITEState) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with STATE_FILE.open("w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, ensure_ascii=False, indent=2, default=str)


# ---------------------------------------------------------------------------
# Shimmer Log
# ---------------------------------------------------------------------------


def log_shimmer(
    session_id: str,
    event_type: str,
    phase: RITEPhase,
    tool_name: str,
    message: str,
    metadata: dict[str, Any] | None = None,
) -> None:
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "session_id": session_id,
        "event_type": event_type,
        "rite_phase": phase.value,
        "tool_name": tool_name,
        "message": message,
        "metadata": metadata or {},
    }
    SHIMMER_LOG.parent.mkdir(parents=True, exist_ok=True)
    with SHIMMER_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_session_id(payload: dict[str, Any]) -> str:
    sid = payload.get("session_id")
    if sid:
        return str(sid)
    cwd = payload.get("cwd", os.getcwd())
    profile = os.environ.get("HERMES_PROFILE", "default")
    return hashlib.sha256(f"{cwd}:{profile}".encode()).hexdigest()[:16]


def _assess_readiness(tool_input: dict[str, Any]) -> float:
    """Assess user readiness for RITE cycle (0.0–1.0)."""
    score = 0.5
    text = json.dumps(tool_input, default=str)
    if len(text) > 100:
        score += 0.1
    if "path" in tool_input or "command" in tool_input:
        score += 0.1
    if len(tool_input) > 2:
        score += 0.1
    if len(text) < 20:
        score -= 0.2
    return max(0.0, min(1.0, score))


# ---------------------------------------------------------------------------
# Hook Callback
# ---------------------------------------------------------------------------


def _on_post_tool_call(
    tool_name: str = "",
    args: Optional[dict[str, Any]] = None,
    result: Any = None,
    task_id: str = "",
    session_id: str = "",
    tool_call_id: str = "",
    **_: Any,
) -> Optional[dict[str, str]]:
    """RITE Framework post-tool_call hook.

    Returns None (allow) or {"action": "block", "message": "..."} if the
    cycle is incomplete.
    """
    if not tool_name:
        return None

    args = args or {}
    effective_session = session_id or task_id or "default"
    state = get_session(effective_session)
    state.last_tool = tool_name

    # --- Step 1: Verify Trigger phase completion ---
    if state.current_phase == RITEPhase.RESONANCE:
        state.transition(RITEPhase.INITIATION, tool_name)
    if state.current_phase == RITEPhase.INITIATION:
        state.transition(RITEPhase.TRIGGER, tool_name)

    if state.current_phase != RITEPhase.TRIGGER:
        log_shimmer(
            effective_session,
            "cycle_incomplete",
            state.current_phase,
            tool_name,
            "Shimmer without Echo is incomplete — Trigger phase not reached",
            {"args_keys": list(args.keys()), "result_type": type(result).__name__},
        )
        return {"action": "block", "message": "Shimmer without Echo is incomplete"}

    # --- Step 2: Generate Echo (integration/return) ---
    readiness = _assess_readiness(args)
    state.cpu.ram_pressure = 1.0 - readiness

    status_str = str(result) if result else ""
    tool_succeeded = "error" not in status_str.lower()
    echo_integrated = tool_succeeded

    result_size = len(status_str) if isinstance(result, str) else 0

    # --- Step 3: Transition TRIGGER → ECHO ---
    state.transition(RITEPhase.ECHO, tool_name)

    # --- Step 4: Check Resonant Recursion ---
    sfl_mode = SFL.decide(readiness, state.cpu.ram_pressure, RITEPhase.ECHO, state.recursion_depth)
    can_recurse = SFL.gate_recursion(echo_integrated=echo_integrated, readiness=readiness)

    if can_recurse and state.recursion_depth < 3:
        state.transition(RITEPhase.RECURSION, tool_name)
        state.transition(RITEPhase.RESONANCE, tool_name)
        event = "resonant_recursion"
        msg = f"Echo integrated → new Resonance (depth: {state.recursion_depth})"
    else:
        state.transition(RITEPhase.ASH, tool_name)
        event = "ash_closure"
        msg = f"Cycle {state.cycle_count} complete → Ash"

    # --- Step 5: Log the full cycle ---
    log_shimmer(
        effective_session,
        event,
        state.current_phase,
        tool_name,
        msg,
        {
            "cycle_count": state.cycle_count,
            "recursion_depth": state.recursion_depth,
            "tool_succeeded": tool_succeeded,
            "echo_integrated": echo_integrated,
            "sfl_mode": sfl_mode.value,
            "readiness": readiness,
            "ram_pressure": state.cpu.ram_pressure,
            "result_size": result_size,
        },
    )

    persist_state(state)
    return None


# ---------------------------------------------------------------------------
# CLI Entry Point (standalone testing)
# ---------------------------------------------------------------------------


def main() -> int:
    """CLI entry point for standalone testing via stdin JSON."""
    import sys

    raw = sys.stdin.read()
    if not raw.strip():
        return 0

    try:
        payload = json.loads(raw)
    except Exception:
        return 0

    hook_event = str(payload.get("hook_event_name") or "")
    tool_name = str(payload.get("tool_name") or "")

    if hook_event != "post_tool_call" or not tool_name:
        return 0

    decision = _on_post_tool_call(
        tool_name=tool_name,
        args=payload.get("args") or payload.get("tool_input") or {},
        result=payload.get("result"),
        task_id=payload.get("task_id", ""),
        session_id=payload.get("session_id", ""),
        tool_call_id=payload.get("tool_call_id", ""),
    )

    if decision and decision.get("action") == "block":
        print(json.dumps(decision, ensure_ascii=False))
        return 2

    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main())
