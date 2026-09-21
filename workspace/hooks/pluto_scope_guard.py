#!/usr/bin/env python3
"""Scope enforcement hook for agent write operations.

Blocks write_file and patch operations that target files outside the agent's
allowed scope. Integrates with the guardian script for canonical validation.

Hook events: pre_tool_call
Matcher: write_file|patch

Input (stdin): JSON payload from Hermes
  {"tool_name": "write_file", "tool_input": {"path": "...", "content": "..."}}
  {"tool_name": "patch", "tool_input": {"path": "...", "old_string": "...", "new_string": "..."}}

Output (stdout): JSON {"action": "block", "message": "..."} or exit 0
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

# Agent-space mapping: profile/canonical -> allowed write root
# Auto-generated from MATRIX/naming-authority.json
AGENT_SPACES = {
    "APPCTX": "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_APPCTX_TRIS",
    "CHAT_EXCAVATION_SCOUT": "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_CHAT_EXCAVATION_SCOUT_TRIS",
    "FACTCHECK": "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_FACTCHECK_TRIS",
    "GODSEYE": "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_GODSEYE_TRIS",
    "HERMESSPL": "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_HERMESSPL_TRIS",
    "JHANOS_ASSESSOR": "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_JHANOS_ASSESSOR_TRIS",
    "JHANOS_BARA": "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_JHANOS_BARA_TRIS",
    "JHANOS_ECHO": "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_JHANOS_ECHO_TRIS",
    "JHANOS_KHEM": "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_JHANOS_KHEM_TRIS",
    "JHANOS_LOMI": "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_JHANOS_LOMI_TRIS",
    "JHANOS_ORON": "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_JHANOS_ORON_TRIS",
    "JHANOS_SYLA": "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_JHANOS_SYLA_TRIS",
    "JHANOS_TARA": "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_JHANOS_TARA_TRIS",
    "JHANOS_VORAK": "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_JHANOS_VORAK_TRIS",
    "JHANOS_ZAYN": "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_JHANOS_ZAYN_TRIS",
    "MEMORY_CURATOR": "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/TRISMIGISTUS/COMPONENTS/agents/MEMORY_CURATOR",
    "ONU": "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_ONU_TRIS",
    "SOLOBIC_SCRIBE": "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_SOLOBIC_SCRIBE_TRIS",
    "SOLOBILITY": "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_SOLOBILITY_TRIS",
    "TCP": "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_TCP_TRIS",
    "TCP_CHECKER": "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_TCP_CHECKER_TRIS",
    "TEMPLATE_EVOLUTION_SCOUT": "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_TEMPLATE_EVOLUTION_SCOUT_TRIS",
}

# Profile name -> canonical mapping
PROFILE_TO_CANONICAL = {
    "appctx": "APPCTX",
    "chatexcavationscout": "CHAT_EXCAVATION_SCOUT",
    "factcheck": "FACTCHECK",
    "godseye": "GODSEYE",
    "hermesspl": "HERMESSPL",
    "jhanosassessor": "JHANOS_ASSESSOR",
    "jhanosbara": "JHANOS_BARA",
    "jhanosecho": "JHANOS_ECHO",
    "jhanoskhem": "JHANOS_KHEM",
    "jhanoslomi": "JHANOS_LOMI",
    "jhanosoron": "JHANOS_ORON",
    "jhanossyla": "JHANOS_SYLA",
    "jhanostara": "JHANOS_TARA",
    "jhanosvorak": "JHANOS_VORAK",
    "jhanoszayn": "JHANOS_ZAYN",
    "memorycurator": "MEMORY_CURATOR",
    "onu": "ONU",
    "solobicscribe": "SOLOBIC_SCRIBE",
    "solobility": "SOLOBILITY",
    "tcp": "TCP",
    "tcpchecker": "TCP_CHECKER",
    "templateevolutionscout": "TEMPLATE_EVOLUTION_SCOUT",
}

# Files no agent may write (governance)
GOVERNANCE_PATHS = [
    "/root/MW_CENTRAL/AGENTS.md",
    "/root/MW_CENTRAL/.hermes.md",
    "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/.hermes.md",
]

# Shared read-only dirs
READ_ONLY_DIRS = [
    "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/MATRIX",
    "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/KNOWLEDGE_LIBRARY",
]

# Identity file patterns (read-only for non-owners)
IDENTITY_PATTERNS = [
    re.compile(r"SOUL.*\.md$"),
    re.compile(r"SCOPE.*\.md$"),
    re.compile(r"config\.yaml$"),
    re.compile(r"state\.md$"),
]

# Curator can write MEMORY.md in all agent-spaces
CURATOR_EXCEPTION = "MEMORY_CURATOR"


def get_canonical() -> str | None:
    """Get canonical name from HERMES_PROFILE env var."""
    profile = os.environ.get("HERMES_PROFILE", "")
    if not profile:
        return None
    return PROFILE_TO_CANONICAL.get(profile.lower())


def block(reason: str) -> int:
    print(json.dumps({"action": "block", "message": reason}, ensure_ascii=False))
    return 2


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except Exception as e:
        # Can't parse — let it through (fail open for safety)
        return 0

    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input") or payload.get("args") or {}

    # Only guard write operations
    if tool_name not in {"write_file", "patch"}:
        return 0

    # Get target path
    if tool_name == "write_file":
        target = str(tool_input.get("path") or "")
    elif tool_name == "patch":
        target = str(tool_input.get("path") or "")
    else:
        return 0

    if not target:
        return 0

    target_path = Path(target).resolve()

    # Get agent's canonical name FIRST
    canonical = get_canonical()
    if not canonical:
        # Unknown profile — allow (root/governance operations)
        return 0

    # Check governance files (only for known agents, not root)
    for gov in GOVERNANCE_PATHS:
        if target_path == Path(gov).resolve():
            return block(f"SCOPE VIOLATION: {Path(target).name} is a governance file — no agent may write")

    # Check read-only shared dirs
    for ro_dir in READ_ONLY_DIRS:
        if str(target_path).startswith(str(Path(ro_dir).resolve())):
            return block(f"SCOPE VIOLATION: {Path(ro_dir).name} is read-only for agents")

    # Get agent's allowed write space
    own_space = AGENT_SPACES.get(canonical)
    if not own_space:
        return 0

    own_space_path = Path(own_space).resolve()

    # Check if target is within own agent-space
    is_own = str(target_path).startswith(str(own_space_path))

    if is_own:
        return 0  # Allowed

    # Target is outside own space — check identity file protection
    target_name = target_path.name
    is_identity = any(p.search(target_name) for p in IDENTITY_PATTERNS)

    if is_identity:
        # Exception: MEMORY_CURATOR can write MEMORY.md everywhere
        if canonical == CURATOR_EXCEPTION and "MEMORY" in target_name:
            return 0
        # Exception: any agent writing to own TRIS identity.md
        if target_name == "identity.md" and is_own:
            return 0
        return block(
            f"SCOPE VIOLATION: {target_name} is an identity file outside your agent-space. "
            f"You may only write inside: {own_space}"
        )

    # Target is another agent's non-identity file
    # Exception: MEMORY_CURATOR can write MEMORY.md in any agent-space
    if canonical == CURATOR_EXCEPTION and "MEMORY" in target_path.name:
        return 0

    for other_canonical, other_space in AGENT_SPACES.items():
        if other_canonical == canonical:
            continue
        if str(target_path).startswith(str(Path(other_space).resolve())):
            return block(
                f"SCOPE VIOLATION: {target} is inside {other_canonical}'s agent-space. "
                f"You may only write inside: {own_space}"
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
