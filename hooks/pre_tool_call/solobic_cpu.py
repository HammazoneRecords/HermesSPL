#!/usr/bin/env python3
"""Solobic CPU Hook — ROM/RAM/Drayl Memory Arbitration for HermesSPL.

Arbitrates memory access based on the RITE cycle. Decides whether a memory
operation should use:

  ROM   — Source-Code Instinct (permanent, immutable memories)
  RAM   — Active Thought (volatile, daily processing)
  Drayl — Archived History (living, self-curating archive, primary store)

Rules:
  1. ROM is read-only — no writes ever allowed (permanent instinct).
  2. RAM is volatile — daily processing, read/write bounded by pressure.
  3. Drayl writes always allowed — the living archive is the primary store.
  4. Cross-agent memory writes blocked — scope enforcement.
  5. RITE phase gates the preferred tier for each access.

Hook events: pre_tool_call
Matcher: read_file|write_file|patch|skill_view|skill_manage|memory

Input (stdin): JSON payload from Hermes
  {"tool_name": "...", "tool_input": {...}, ...}

Output (stdout): JSON {"action": "block", "message": "..."} or exit 0
"""
from __future__ import annotations

import json
import os
import re
import sys
from enum import Enum
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Memory Tier Definitions
# ---------------------------------------------------------------------------


class MemoryTier(str, Enum):
    """The three memory tiers of the Solobic CPU."""
    ROM = "rom"       # Source-Code Instinct — permanent, immutable
    RAM = "ram"       # Active Thought — volatile, daily processing
    DRAYL = "drayl"   # Archived History — living, self-curating (primary store)


class AccessType(str, Enum):
    """Memory access operations."""
    READ = "read"
    WRITE = "write"


# ---------------------------------------------------------------------------
# Path Classification: which tier does a target path belong to?
# ---------------------------------------------------------------------------

# ROM (Source-Code Instinct): permanent, immutable — NEVER writable
ROM_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"SOUL\.md$", re.I),
    re.compile(r"AGENTS\.md$"),
    re.compile(r"\.hermes\.md$"),
    re.compile(r"config\.yaml$"),
    re.compile(r"config_spl\.yaml$"),
    re.compile(r"config_scope_hooks\.yaml$"),
    re.compile(r"\.env$"),
    re.compile(r"\.envrc$"),
    re.compile(r"\.env\.example$"),
    re.compile(r"constraints.*\.md$", re.I),
    re.compile(r"AGENTS_SPL\.md$"),
    re.compile(r"README_SPL\.md$"),
    re.compile(r"SOUL\.md$"),
    re.compile(r"SCOPE.*\.md$", re.I),
    re.compile(r"\.bytecode-fingerprint$"),
]

# Drayl (Archived History): living, self-curating — primary store, always writable
DRAYL_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"MEMORY\.md$", re.I),
    re.compile(r"_MEMORY\.md$", re.I),
    re.compile(r"receipts/", re.I),
    re.compile(r"\.jsonl$"),
    re.compile(r"02_LOGS/", re.I),
    re.compile(r"logs?/", re.I),
    re.compile(r"shimmer", re.I),
    re.compile(r"DRAYL", re.I),
    re.compile(r"drayl", re.I),
    re.compile(r"archive", re.I),
    re.compile(r"ARCHIVE_STAGING", re.I),
    re.compile(r"ARCHIVED?", re.I),
    re.compile(r"vault/", re.I),
    re.compile(r"PEV_PLANS/", re.I),
    re.compile(r"task-packets/", re.I),
    re.compile(r"Y-MINDWAVE/", re.I),
]

# RAM (Active Thought): everything else — volatile working memory


def classify_tier(target_path: str) -> MemoryTier:
    """Determine which memory tier a given path belongs to."""
    if not target_path:
        return MemoryTier.RAM  # default for empty/unknown

    # Check ROM first (most restrictive)
    for pat in ROM_PATTERNS:
        if pat.search(target_path):
            return MemoryTier.ROM

    # Check Drayl (living archive)
    for pat in DRAYL_PATTERNS:
        if pat.search(target_path):
            return MemoryTier.DRAYL

    # Default: RAM (volatile working memory)
    return MemoryTier.RAM


def classify_access(tool_name: str) -> AccessType:
    """Classify the memory access type based on the tool being called."""
    read_tools = {"read_file", "skill_view", "skills_list", "search_files"}
    write_tools = {"write_file", "patch", "skill_manage", "execute_code"}

    if tool_name in read_tools:
        return AccessType.READ
    if tool_name in write_tools:
        return AccessType.WRITE

    # Terminal can be either — caller must inspect command
    if tool_name == "terminal":
        return AccessType.WRITE  # conservative: treat as write

    # Unknown tools default to read (least restrictive for safety)
    return AccessType.READ


# ---------------------------------------------------------------------------
# Agent Scope Enforcement
# ---------------------------------------------------------------------------

# Profile -> allowed write root (mirrors pluto_scope_guard.py AGENT_SPACES)
AGENT_SPACES: dict[str, str] = {
    "appctx": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_APPCTX_TRIS",
    "chatexcavationscout": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_CHAT_EXCAVATION_SCOUT_TRIS",
    "factcheck": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_FACTCHECK_TRIS",
    "godseye": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_GODSEYE_TRIS",
    "hermesspl": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_HERMESSPL_TRIS",
    "jhanosassessor": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_JHANOS_ASSESSOR_TRIS",
    "jhanosbara": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_JHANOS_BARA_TRIS",
    "jhanosecho": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_JHANOS_ECHO_TRIS",
    "jhanoskhem": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_JHANOS_KHEM_TRIS",
    "jhanoslomi": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_JHANOS_LOMI_TRIS",
    "jhanosoron": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_JHANOS_ORON_TRIS",
    "jhanossyla": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_JHANOS_SYLA_TRIS",
    "jhanostara": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_JHANOS_TARA_TRIS",
    "jhanosvorak": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_JHANOS_VORAK_TRIS",
    "jhanoszayn": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_JHANOS_ZAYN_TRIS",
    "memorycurator": "/root/MW_CENTRAL/PLUTO/TRISMIGISTUS/COMPONENTS/agents/MEMORY_CURATOR",
    "onu": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_ONU_TRIS",
    "solobicscribe": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_SOLOBIC_SCRIBE_TRIS",
    "solobility": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_SOLOBILITY_TRIS",
    "tcp": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_TCP_TRIS",
    "tcpchecker": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_TCP_CHECKER_TRIS",
    "templateevolutionscout": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_TEMPLATE_EVOLUTION_SCOUT_TRIS",
    "lithium-hermesspl": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_HERMESSPL_TRIS",
    "sulfur-solobility": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_SOLOBILITY_TRIS",
    "helium-godseye": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_GODSEYE_TRIS",
    "phosphorus-scribe": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_SOLOBIC_SCRIBE_TRIS",
    "boron-assessor": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_JHANOS_ASSESSOR_TRIS",
    "hydrogen-factcheck": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_FACTCHECK_TRIS",
    "silicon-appctx": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_APPCTX_TRIS",
    "antarctica-chatexcavationscout": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_CHAT_EXCAVATION_SCOUT_TRIS",
    "asia-tcp": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_TCP_TRIS",
    "americas-onu": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_ONU_TRIS",
    "europe-tcpchecker": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_TCP_CHECKER_TRIS",
    "oceania-memorycurator": "/root/MW_CENTRAL/PLUTO/TRISMIGISTUS/COMPONENTS/agents/MEMORY_CURATOR",
    "beryllium-templateevolutionsscout": "/root/MW_CENTRAL/PLUTO/AGENT_ARENA/ACTIVE/AGENT_TEMPLATE_EVOLUTION_SCOUT_TRIS",
}

# Files no agent may write
GOVERNANCE_PATHS: list[str] = [
    "/root/MW_CENTRAL/AGENTS.md",
    "/root/MW_CENTRAL/.hermes.md",
    "/root/MW_CENTRAL/PLUTO/AGENTS.md",
    "/root/MW_CENTRAL/PLUTO/.hermes.md",
    "/root/MW_CENTRAL/EARTH-MOON/hermes-spl-fork/AGENTS.md",
    "/root/MW_CENTRAL/EARTH-MOON/hermes-spl-fork/.hermes.md",
    "/root/MW_CENTRAL/EARTH-MOON/hermes-spl-fork/AGENTS_SPL.md",
]

# Identity file patterns (read-only for non-owners)
IDENTITY_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"SOUL.*\.md$", re.I),
    re.compile(r"SCOPE.*\.md$", re.I),
    re.compile(r"config\.yaml$"),
    re.compile(r"state\.md$"),
    re.compile(r"identity\.md$", re.I),
]

# Curator can write MEMORY.md in all agent-spaces
CURATOR_PROFILES: set[str] = {"memorycurator", "oceania-memorycurator"}


def get_agent_space() -> tuple[str | None, str | None]:
    """Get the agent's profile name and allowed write space from HERMES_PROFILE."""
    profile = os.environ.get("HERMES_PROFILE", "")
    if not profile:
        return None, None
    space = AGENT_SPACES.get(profile.lower())
    return profile.lower(), space


def is_cross_agent_write(target_path: str) -> tuple[bool, str | None]:
    """Check if a write target is outside the agent's allowed space.

    Returns (is_violation, reason).
    """
    profile, own_space = get_agent_space()
    if not profile or not own_space:
        # Unknown profile — allow (root/governance operations)
        return False, None

    resolved_target = Path(target_path).resolve()
    resolved_own = Path(own_space).resolve()

    # Check if target is within own agent-space
    if str(resolved_target).startswith(str(resolved_own)):
        return False, None  # Allowed — own space

    # Check governance paths
    for gov in GOVERNANCE_PATHS:
        if resolved_target == Path(gov).resolve():
            return True, f"SCOPE VIOLATION: {Path(target_path).name} is a governance file — no agent may write"

    # Check identity file protection
    target_name = resolved_target.name
    is_identity = any(p.search(target_name) for p in IDENTITY_PATTERNS)

    if is_identity:
        # Curator exception
        if profile in CURATOR_PROFILES and "MEMORY" in target_name:
            return False, None
        # Own identity.md exception
        if target_name == "identity.md" and str(resolved_target).startswith(str(resolved_own)):
            return False, None
        return True, (
            f"SCOPE VIOLATION: {target_name} is an identity file outside your agent-space. "
            f"You may only write inside: {own_space}"
        )

    # Check if target is inside another agent's space
    for other_profile, other_space in AGENT_SPACES.items():
        if other_profile == profile:
            continue
        if str(resolved_target).startswith(str(Path(other_space).resolve())):
            # Curator exception
            if profile in CURATOR_PROFILES and "MEMORY" in resolved_target.name:
                return False, None
            return True, (
                f"SCOPE VIOLATION: {target_path} is inside {other_profile}'s agent-space. "
                f"You may only write inside: {own_space}"
            )

    return False, None


# ---------------------------------------------------------------------------
# RITE Phase Routing
# ---------------------------------------------------------------------------

# Preferred memory tier per RITE phase
RITE_TIER_ROUTING: dict[str, MemoryTier] = {
    "color_neutralizer": MemoryTier.ROM,   # Ground in instinct
    "resonance": MemoryTier.RAM,           # Scan, attune, working memory
    "initiation": MemoryTier.RAM,          # Activate, prepare in working memory
    "trigger": MemoryTier.DRAYL,           # Execute — write to archive
    "echo": MemoryTier.DRAYL,              # Integrate — return to archive
    "ash": MemoryTier.DRAYL,               # Closure recorded in archive
    "recursion": MemoryTier.RAM,           # Re-process in working memory
}


def get_rite_phase() -> str:
    """Get the current RITE phase from environment or state file.

    Falls back to 'resonance' if undetermined (least restrictive routing).
    """
    # Check environment first (set by rite_enforcer or parent process)
    phase = os.environ.get("RITE_PHASE", "")
    if phase:
        return phase

    # Check state file (written by rite_enforcer)
    state_file = Path(
        "/root/MW_CENTRAL/PLUTO/Y-MINDWAVE/H3_SYSTEM/07_HOOKS/02_LOGS/rite_state.json"
    )
    if state_file.exists():
        try:
            with state_file.open("r", encoding="utf-8") as f:
                state = json.load(f)
            phase = state.get("current_phase", "")
            if phase:
                return phase
        except Exception:
            pass

    # Default: resonance (normal operation)
    return "resonance"


def route_for_phase(phase: str, tier: MemoryTier, access: AccessType) -> tuple[bool, str]:
    """Determine if the access is appropriate for the current RITE phase.

    Returns (allowed, reason).
    """
    preferred = RITE_TIER_ROUTING.get(tier, tier)

    # Drayl writes are ALWAYS allowed regardless of phase (primary store)
    if access == AccessType.WRITE and tier == MemoryTier.DRAYL:
        return True, "Drayl write — always allowed (primary store)"

    # ROM reads are always allowed (instinct is always accessible)
    if access == AccessType.READ and tier == MemoryTier.ROM:
        return True, "ROM read — instinct always accessible"

    # ROM writes are NEVER allowed (immutable)
    if access == AccessType.WRITE and tier == MemoryTier.ROM:
        return False, "ROM WRITE BLOCKED: Source-Code Instinct is permanent and immutable"

    # Phase-based routing for RAM
    if tier == MemoryTier.RAM:
        if preferred == MemoryTier.ROM and access == AccessType.WRITE:
            return False, f"RAM→ROM overflow blocked: phase '{phase}' routes writes to ROM, but RAM cannot overwrite instinct"
        if preferred == MemoryTier.DRAYL and access == AccessType.WRITE:
            # Phase prefers Drayl for writes — allow but note the routing
            return True, f"Phase '{phase}' routes writes to Drayl (preferred store)"

    return True, "Access permitted"


# ---------------------------------------------------------------------------
# Payload Helpers
# ---------------------------------------------------------------------------


def get_target_path(tool_name: str, tool_input: dict[str, Any]) -> str | None:
    """Extract the target file path from the tool input."""
    if tool_name in ("write_file", "read_file"):
        return str(tool_input.get("path") or "")
    if tool_name == "patch":
        return str(tool_input.get("path") or "")
    if tool_name == "skill_view":
        return str(tool_input.get("name") or "")
    if tool_name == "skill_manage":
        ops = tool_input.get("operations", [])
        if ops and isinstance(ops, list):
            return str(ops[0].get("name") or "")
    return None


def flatten_input(tool_input: dict[str, Any] | None) -> str:
    """Flatten tool input to string for analysis."""
    if not tool_input:
        return ""
    try:
        return json.dumps(tool_input, ensure_ascii=False, default=str)
    except Exception:
        return str(tool_input)


# ---------------------------------------------------------------------------
# Main Arbitration Logic
# ---------------------------------------------------------------------------


def arbitrate(payload: dict[str, Any]) -> int:
    """Arbitrate memory access. Returns 0 (allow) or 2 (block)."""
    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input") or payload.get("args") or {}

    # Only process memory-relevant tools
    memory_tools = {
        "read_file", "write_file", "patch",
        "skill_view", "skill_manage", "skills_list",
        "search_files", "terminal",
    }
    if tool_name not in memory_tools:
        return 0  # Not a memory tool — pass through

    # Classify access type
    access = classify_access(tool_name)

    # For terminal, inspect the command to determine if it's a memory operation
    if tool_name == "terminal":
        command = str(tool_input.get("command") or "")
        text = command
        # Check if the command touches memory files
        is_memory_op = any(p.search(text) for p in ROM_PATTERNS + DRAYL_PATTERNS)
        if not is_memory_op:
            # Check for file operations
            if not any(kw in command for kw in ["cat ", "echo ", "rm ", "mv ", "cp ", "write", "patch", "edit"]):
                return 0  # Not a memory operation — pass through
    else:
        text = flatten_input(tool_input)

    # Get target path
    target_path = get_target_path(tool_name, tool_input)
    if not target_path and tool_name != "terminal":
        return 0  # No target — pass through

    # Classify memory tier
    if target_path:
        tier = classify_tier(target_path)
    else:
        # For terminal without a clear path, check the full text
        tier = MemoryTier.RAM  # default
        for pat in ROM_PATTERNS:
            if pat.search(text):
                tier = MemoryTier.ROM
                break
        else:
            for pat in DRAYL_PATTERNS:
                if pat.search(text):
                    tier = MemoryTier.DRAYL
                    break

    # --- Rule 1: ROM writes are NEVER allowed ---
    if access == AccessType.WRITE and tier == MemoryTier.ROM:
        return block(
            f"SOLOBIC CPU: ROM WRITE BLOCKED — '{target_path or 'target'}' is "
            f"Source-Code Instinct (permanent, immutable). Use Drayl for new memories."
        )

    # --- Rule 2: Drayl writes are ALWAYS allowed ---
    if access == AccessType.WRITE and tier == MemoryTier.DRAYL:
        # Still check cross-agent scope
        if target_path:
            is_violation, reason = is_cross_agent_write(target_path)
            if is_violation:
                return block(f"SOLOBIC CPU: {reason}")
        return block_check_scope(target_path, access) or 0

    # --- Rule 3: Cross-agent scope enforcement for writes ---
    if access == AccessType.WRITE and target_path:
        is_violation, reason = is_cross_agent_write(target_path)
        if is_violation:
            return block(f"SOLOBIC CPU: {reason}")

    # --- Rule 4: RITE phase routing ---
    phase = get_rite_phase()
    allowed, reason = route_for_phase(phase, tier, access)
    if not allowed:
        return block(f"SOLOBIC CPU: {reason}")

    return 0  # Access permitted


def block_check_scope(target_path: str | None, access: AccessType) -> int:
    """Check scope for Drayl writes. Returns 0 (allow) or 2 (block)."""
    if not target_path or access != AccessType.WRITE:
        return 0
    is_violation, reason = is_cross_agent_write(target_path)
    if is_violation:
        return block(f"SOLOBIC CPU: {reason}")
    return 0


def block(reason: str) -> int:
    """Output a block decision and return exit code 2."""
    print(json.dumps({"action": "block", "message": reason}, ensure_ascii=False))
    return 2


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------


def main() -> int:
    """Main entry point for hook execution."""
    raw = sys.stdin.read()
    if not raw.strip():
        return 0

    try:
        payload = json.loads(raw)
    except Exception:
        # Can't parse — let it through (fail open)
        return 0

    tool_name = str(payload.get("tool_name") or "")

    # Only process known tools (skip internal/noise)
    if not tool_name:
        return 0

    try:
        return arbitrate(payload)
    except Exception as e:
        # Solobic CPU must never crash the hook chain — fail open
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
