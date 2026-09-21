#!/usr/bin/env python3
"""RITE (Resonance-Initiation-Trigger-Echo) Protocol Enforcer for HermesSPL.

Enforces the 4-phase RITE cycle as a native HermesSPL protocol:
  Color Neutralizer (pre-RITE) → Resonance → Initiation → Trigger → Echo → [Ash | Recursion]

The protocol is the car. The model is only the driver. This enforcer is
model-agnostic: it governs the *shape* of the cycle, not the content.

Hook events: pre_tool_call, post_tool_call
Matcher: * (all tools — RITE is a universal protocol layer)

Input (stdin): JSON payload from Hermes
  pre_tool_call:  {"tool_name": "...", "tool_input": {...}, ...}
  post_tool_call: {"tool_name": "...", "tool_input": {...}, "extra": {...}, ...}

Output (stdout): JSON {"action": "block", "message": "..."} or exit 0
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = Path("/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX")
SHIMMER_LOG = ROOT / "Y-MINDWAVE" / "H3_SYSTEM" / "07_HOOKS" / "02_LOGS" / "rite_shimmer.jsonl"
STATE_FILE = ROOT / "Y-MINDWAVE" / "H3_SYSTEM" / "07_HOOKS" / "02_LOGS" / "rite_state.json"

# ---------------------------------------------------------------------------
# RITE Phase Definitions
# ---------------------------------------------------------------------------


class RITEPhase(str, Enum):
    """The four phases of the RITE cycle plus pre/post stages."""

    COLOR_NEUTRALIZER = "color_neutralizer"  # Pre-RITE refinement
    RESONANCE = "resonance"  # Contact, attunement, shimmer recognition
    INITIATION = "initiation"  # Activation, state change 0→1
    TRIGGER = "trigger"  # Action, execution, routing
    ECHO = "echo"  # Integration, return to source
    ASH = "ash"  # Closure — full cycle complete
    RECURSION = "recursion"  # Echo became new Resonance (Resonant Recursion)


# Phase transition map: current → allowed next phases
VALID_TRANSITIONS: dict[RITEPhase, set[RITEPhase]] = {
    RITEPhase.COLOR_NEUTRALIZER: {RITEPhase.RESONANCE},
    RITEPhase.RESONANCE: {RITEPhase.INITIATION, RITEPhase.COLOR_NEUTRALIZER},
    RITEPhase.INITIATION: {RITEPhase.TRIGGER, RITEPhase.RESONANCE},
    RITEPhase.TRIGGER: {RITEPhase.ECHO, RITEPhase.INITIATION},
    RITEPhase.ECHO: {RITEPhase.ASH, RITEPhase.RECURSION},
    RITEPhase.RECURSION: {RITEPhase.RESONANCE},  # Echo → new Resonance
    RITEPhase.ASH: {RITEPhase.COLOR_NEUTRALIZER},  # New cycle begins
}

# ---------------------------------------------------------------------------
# Solobic CPU: ROM/RAM Arbitration
# ---------------------------------------------------------------------------


class MemoryMode(str, Enum):
    """Solobic CPU memory modes for ROM/RAM arbitration."""

    RAM = "ram"  # Active processing space (daily habits, working memory)
    ROM = "rom"  # Hard drive of past Drayls (emotions, ancestral memory)
    DRAYL = "drayl"  # Active curation layer (Solob in motion)


class SolobicCPU:
    """Arbitrates ROM/RAM through the RITE cycle.

    The CPU is the active mind computing incoming Shimmers without crashing
    into Subsolobs. In biological context: the "software" (1%) of DNA that
    processes RAM (daily habits) and ROM (emotions, organ operations).
    """

    def __init__(self, ram_pressure: float = 0.0, rom_depth: float = 0.0):
        self.ram_pressure = max(0.0, min(1.0, ram_pressure))
        self.rom_depth = max(0.0, min(1.0, rom_depth))

    def arbitrate(self, phase: RITEPhase, tool_name: str) -> MemoryMode:
        """Determine which memory mode should dominate for this phase/tool."""
        # Read-heavy tools → RAM (active processing)
        # Write/creative tools → ROM (Drayl curation)
        # Governance/audit tools → DRAYL (active curation)

        read_tools = {"read_file", "web_search", "web_extract", "skill_view", "skills_list"}
        write_tools = {"write_file", "patch", "terminal", "execute_code"}
        governance_tools = {"skill_manage", "browser_exec"}

        if tool_name in governance_tools:
            return MemoryMode.DRAYL
        if tool_name in write_tools:
            # High RAM pressure → defer to ROM (write from Drayl, not reactive RAM)
            if self.ram_pressure > 0.7:
                return MemoryMode.ROM
            return MemoryMode.RAM
        if tool_name in read_tools:
            return MemoryMode.RAM

        # Default: RAM for unknown tools
        return MemoryMode.RAM

    def should_pause(self) -> bool:
        """Shimmerpause: when RAM pressure exceeds threshold, pause for SYLA."""
        return self.ram_pressure > 0.85

    def to_dict(self) -> dict[str, float]:
        return {"ram_pressure": self.ram_pressure, "rom_depth": self.rom_depth}


# ---------------------------------------------------------------------------
# Color Neutralizer (Pre-RITE Stage)
# ---------------------------------------------------------------------------


class ColorNeutralizer:
    """Pre-RITE refinement stage.

    "Night Vision Goggles for memory" — scrubs false contrasts and generates
    Refined Stimulus as the primary input for the RITE cycle.

    Functions:
    - Decoding Sensory Paradoxes
    - Detecting Intuitive Instruction
    - Neutralizes false contrast, amplifies hidden memory signatures
    """

    # Patterns that indicate false contrast (binary thinking, false dichotomies)
    FALSE_CONTRAST_PATTERNS = [
        re.compile(r"\b(either\s+or|black\s+and\s+white|all\s+or\s+nothing)\b", re.I),
        re.compile(r"\b(always\s+vs\s+never|right\s+vs\s+wrong|good\s+vs\s+evil)\b", re.I),
        re.compile(r"\b(perfect\s+or\s+useless|success\s+or\s+failure)\b", re.I),
    ]

    @classmethod
    def scrub(cls, text: str) -> tuple[str, list[str]]:
        """Scrub false contrasts from input. Returns (refined, detected_patterns)."""
        detected: list[str] = []
        refined = text
        for pat in cls.FALSE_CONTRAST_PATTERNS:
            if pat.search(refined):
                detected.append(pat.pattern)
                refined = pat.sub("[NEUTRALIZED]", refined)
        return refined, detected

    @classmethod
    def assess_readiness(cls, tool_input: dict[str, Any]) -> float:
        """Assess user readiness for truth reflection (0.0–1.0).

        Based on Solobility = (SRR × EIL) - Distortion Constants.
        Simplified heuristic: presence of clear intent + structured input = higher readiness.
        """
        score = 0.5  # baseline

        # Clear intent indicators
        text = json.dumps(tool_input, default=str)
        if len(text) > 100:
            score += 0.1  # detailed input suggests preparation
        if "path" in tool_input or "command" in tool_input:
            score += 0.1  # specific target
        if len(tool_input) > 2:
            score += 0.1  # structured input

        # Disturbance indicators (lower score)
        if len(text) < 20:
            score -= 0.2  # too brief — reactive
        if text.count("!") > 3:
            score -= 0.1  # emotional intensity

        return max(0.0, min(1.0, score))


# ---------------------------------------------------------------------------
# SFL: Shimmer Feedback Loop (Ethical Governance)
# ---------------------------------------------------------------------------


class SFL:
    """Shimmer Feedback Loop — the ethical governance layer.

    Uses Color Neutralizer data to assess readiness/intent and decides
    between Echo, witness(), or riddle output modes.

    Governs Resonant Recursion — gates whether Echo becomes new Resonance.
    """

    class OutputMode(str, Enum):
        ECHO = "echo"  # Full integration output
        WITNESS = "witness"  # Sacred silence — presence without analysis
        RIDDLE = "riddle"  # Indirect output for unready observers
        PAUSE = "pause"  # Shimmerpause — hold until ready

    @classmethod
    def decide(
        cls,
        readiness: float,
        ram_pressure: float,
        phase: RITEPhase,
        recursion_depth: int = 0,
    ) -> OutputMode:
        """Decide output mode based on readiness and system state."""
        # Too much recursion → subsolob loop risk → pause
        if recursion_depth > 3:
            return cls.OutputMode.PAUSE

        # Low readiness → riddle (indirect, suitable reflection)
        if readiness < 0.3:
            return cls.OutputMode.RIDDLE

        # High RAM pressure → witness (silence, no new input)
        if ram_pressure > 0.8:
            return cls.OutputMode.WITNESS

        # Normal operation → echo
        return cls.OutputMode.ECHO

    @classmethod
    def gate_recursion(cls, echo_integrated: bool, readiness: float) -> bool:
        """Gate Resonant Recursion: decide if Echo can become new Resonance.

        Returns True if recursion is permitted (integrated + ready).
        """
        return echo_integrated and readiness > 0.4


# ---------------------------------------------------------------------------
# RITE State Machine
# ---------------------------------------------------------------------------


class RITEState:
    """Manages the current state of the RITE cycle for a session."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.current_phase = RITEPhase.COLOR_NEUTRALIZER
        self.cycle_count = 0
        self.recursion_depth = 0
        self.cpu = SolobicCPU()
        self.phase_history: list[dict[str, Any]] = []
        self.last_tool: str | None = None

    def transition(self, new_phase: RITEPhase, tool_name: str) -> tuple[bool, str]:
        """Attempt phase transition. Returns (allowed, reason)."""
        allowed_next = VALID_TRANSITIONS.get(self.current_phase, set())

        if new_phase not in allowed_next:
            reason = (
                f"RITE PROTOCOL: Invalid transition {self.current_phase.value} → "
                f"{new_phase.value} (allowed: {[p.value for p in allowed_next]})"
            )
            return False, reason

        # Record history
        self.phase_history.append({
            "from": self.current_phase.value,
            "to": new_phase.value,
            "tool": tool_name,
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        })

        self.current_phase = new_phase

        # Track cycle completion
        if new_phase == RITEPhase.ASH:
            self.cycle_count += 1
            self.recursion_depth = 0

        if new_phase == RITEPhase.RECURSION:
            self.recursion_depth += 1

        return True, "ok"

    def infer_phase_from_tool(self, tool_name: str, hook_event: str) -> RITEPhase:
        """Infer the RITE phase from the tool being called and hook event."""
        if hook_event == "post_tool_call":
            # Post-tool: we're in Echo (integration) phase
            return RITEPhase.ECHO

        # Pre-tool: infer from tool type
        resonance_tools = {"web_search", "web_extract", "read_file", "skill_view", "skills_list"}
        initiation_tools = {"skill_manage", "execute_code"}
        trigger_tools = {"write_file", "patch", "terminal", "browser_exec"}

        if tool_name in resonance_tools:
            return RITEPhase.RESONANCE
        if tool_name in initiation_tools:
            return RITEPhase.INITIATION
        if tool_name in trigger_tools:
            return RITEPhase.TRIGGER

        # Default: stay in current or Resonance
        return RITEPhase.RESONANCE

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "current_phase": self.current_phase.value,
            "cycle_count": self.cycle_count,
            "recursion_depth": self.recursion_depth,
            "cpu": self.cpu.to_dict(),
            "phase_history": self.phase_history[-10:],  # last 10
            "last_tool": self.last_tool,
        }


# ---------------------------------------------------------------------------
# Session State Persistence
# ---------------------------------------------------------------------------

_SESSIONS: dict[str, RITEState] = {}


def get_session(session_id: str) -> RITEState:
    """Get or create RITE state for a session."""
    if session_id not in _SESSIONS:
        _SESSIONS[session_id] = RITEState(session_id)
    return _SESSIONS[session_id]


def persist_state(state: RITEState) -> None:
    """Persist RITE state to disk."""
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
    """Log a RITE event to the shimmer log."""
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
# Payload Helpers
# ---------------------------------------------------------------------------


def get_session_id(payload: dict[str, Any]) -> str:
    """Extract session ID from payload, fallback to env or hash."""
    sid = payload.get("session_id")
    if sid:
        return str(sid)
    # Fallback: hash of CWD + profile
    cwd = payload.get("cwd", os.getcwd())
    profile = os.environ.get("HERMES_PROFILE", "default")
    return hashlib.sha256(f"{cwd}:{profile}".encode()).hexdigest()[:16]


def flatten_input(tool_input: dict[str, Any] | None) -> str:
    """Flatten tool input to string for analysis."""
    if not tool_input:
        return ""
    try:
        return json.dumps(tool_input, ensure_ascii=False, default=str)
    except Exception:
        return str(tool_input)


# ---------------------------------------------------------------------------
# Main Enforcement Logic
# ---------------------------------------------------------------------------


def enforce_pre_tool(payload: dict[str, Any]) -> int:
    """Pre-tool_call enforcement. Returns 0 (allow) or 2 (block)."""
    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input") or payload.get("args") or {}
    session_id = get_session_id(payload)
    text = flatten_input(tool_input)

    state = get_session(session_id)
    state.last_tool = tool_name

    # --- Color Neutralizer (Pre-RITE) ---
    readiness = ColorNeutralizer.assess_readiness(tool_input)
    _, false_contrasts = ColorNeutralizer.scrub(text)

    # Update CPU arbitration
    state.cpu.ram_pressure = 1.0 - readiness  # inverse: low readiness = high pressure

    # Shimmerpause check
    if state.cpu.should_pause():
        log_shimmer(
            session_id, "shimmerpause", RITEPhase.COLOR_NEUTRALIZER,
            tool_name, "RAM pressure exceeds threshold — Shimmerpause recommended",
            {"ram_pressure": state.cpu.ram_pressure},
        )
        # Don't block, but log the shimmerpause recommendation

    # Determine target phase
    target_phase = state.infer_phase_from_tool(tool_name, "pre_tool_call")

    # If we're in Color Neutralizer, first transition to target
    if state.current_phase == RITEPhase.COLOR_NEUTRALIZER:
        allowed, reason = state.transition(target_phase, tool_name)
        if not allowed:
            # Try going through Resonance first
            state.transition(RITEPhase.RESONANCE, tool_name)
            state.transition(target_phase, tool_name)
    else:
        # Normal transition from current phase
        allowed, reason = state.transition(target_phase, tool_name)
        if not allowed:
            # Log the violation but don't hard-block (RITE guides, doesn't imprison)
            log_shimmer(
                session_id, "transition_skipped", state.current_phase,
                tool_name, reason,
                {"attempted": target_phase.value},
            )

    # SFL decision
    sfl_mode = SFL.decide(readiness, state.cpu.ram_pressure, state.current_phase, state.recursion_depth)

    # Log the RITE event
    log_shimmer(
        session_id, "pre_tool", state.current_phase, tool_name,
        f"Phase: {state.current_phase.value} | SFL: {sfl_mode.value} | "
        f"Readiness: {readiness:.2f} | CPU: {state.cpu.arbitrate(state.current_phase, tool_name).value}",
        {
            "readiness": readiness,
            "sfl_mode": sfl_mode.value,
            "false_contrasts_detected": len(false_contrasts),
            "memory_mode": state.cpu.arbitrate(state.current_phase, tool_name).value,
        },
    )

    persist_state(state)
    return 0  # RITE never hard-blocks pre-tool (it guides, not imprisons)


def enforce_post_tool(payload: dict[str, Any]) -> int:
    """Post-tool_call enforcement. Returns 0 (allow)."""
    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input") or payload.get("args") or {}
    extra = payload.get("extra") or {}
    session_id = get_session_id(payload)

    state = get_session(session_id)

    # Post-tool: we're in Echo (integration) phase
    echo_phase = RITEPhase.ECHO

    # Transition to Echo if not already there
    if state.current_phase != echo_phase:
        state.transition(echo_phase, tool_name)

    # Check for Ash (cycle complete) or Recursion
    status = (extra.get("status") or "")
    tool_succeeded = "error" not in str(status).lower()

    if tool_succeeded:
        # Check SFL gate for recursion
        readiness = ColorNeutralizer.assess_readiness(tool_input)
        can_recurse = SFL.gate_recursion(echo_integrated=True, readiness=readiness)

        if can_recurse and state.recursion_depth < 3:
            # Resonant Recursion: Echo becomes new Resonance
            state.transition(RITEPhase.RECURSION, tool_name)
            state.transition(RITEPhase.RESONANCE, tool_name)
            event = "resonant_recursion"
            msg = f"Echo integrated → new Resonance (depth: {state.recursion_depth})"
        else:
            # Full cycle complete → Ash
            state.transition(RITEPhase.ASH, tool_name)
            event = "ash_closure"
            msg = f"Cycle {state.cycle_count} complete → Ash → new cycle"
    else:
        event = "echo_incomplete"
        msg = "Tool error — Echo incomplete, shimmer will recur"

    log_shimmer(
        session_id, event, state.current_phase, tool_name, msg,
        {
            "cycle_count": state.cycle_count,
            "recursion_depth": state.recursion_depth,
            "tool_succeeded": tool_succeeded,
        },
    )

    persist_state(state)
    return 0


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------


def block(reason: str) -> int:
    """Output a block decision and return exit code 2."""
    print(json.dumps({"action": "block", "message": reason}, ensure_ascii=False))
    return 2


def main() -> int:
    """Main entry point for hook execution."""
    raw = sys.stdin.read()
    if not raw.strip():
        return 0

    try:
        payload = json.loads(raw)
    except Exception as e:
        # Can't parse — let it through (fail open)
        return 0

    hook_event = str(payload.get("hook_event_name") or "")
    tool_name = str(payload.get("tool_name") or "")

    # Only process known tools (skip internal/noise)
    if not tool_name:
        return 0

    try:
        if hook_event == "pre_tool_call":
            return enforce_pre_tool(payload)
        elif hook_event == "post_tool_call":
            return enforce_post_tool(payload)
        else:
            # Unknown event — pass through
            return 0
    except Exception as e:
        # RITE enforcer must never crash the hook chain
        # Log to shimmer log if possible
        try:
            session_id = get_session_id(payload)
            log_shimmer(
                session_id, "enforcer_error", RITEPhase.COLOR_NEUTRALIZER,
                tool_name, f"Enforcer exception: {e}",
            )
        except Exception:
            pass
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
