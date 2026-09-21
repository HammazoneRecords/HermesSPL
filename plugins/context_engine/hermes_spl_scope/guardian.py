"""HermesSPL Scope Guardian — runtime enforcement engine.

Validates write operations against agent scope boundaries.
Loaded by the context_engine plugin on session start.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Optional, Tuple

BASE = Path("/root/MW_CENTRAL")
ANDROMALIUS = BASE / "ANDROMALIUS"

# Agent-space mapping (canonical name -> absolute path)
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

# Profile -> canonical
PROFILE_TO_CANONICAL = {k.lower(): k for k in AGENT_SPACES}

# Governance files (no agent may write)
GOVERNANCE_PATHS = [
    BASE / "AGENTS.md",
    BASE / ".hermes.md",
    BASE / "ANDROMALIUS/.hermes.md",
]

# Shared read-only dirs
READ_ONLY_DIRS = [
    BASE / "ANDROMALIUS/MATRIX",
    BASE / "ANDROMALIUS/KNOWLEDGE_LIBRARY",
]

# Identity file patterns
IDENTITY_PATTERNS = [
    re.compile(r"SOUL.*\.md$"),
    re.compile(r"SCOPE.*\.md$"),
    re.compile(r"config\.yaml$"),
    re.compile(r"state\.md$"),
]

CURATOR = "MEMORY_CURATOR"


def get_canonical() -> Optional[str]:
    """Get canonical name from HERMES_PROFILE env var."""
    profile = os.environ.get("HERMES_PROFILE", "")
    if not profile:
        return None
    return PROFILE_TO_CANONICAL.get(profile.lower())


class SplScopeGuardian:
    """Validates agent write operations against scope boundaries."""

    def check_write(self, target: str) -> Tuple[bool, Optional[str], Optional[dict]]:
        """Check if current agent can write to target.
        
        Returns: (blocked, block_message, modified_input)
        """
        target_path = Path(target).resolve()
        canonical = get_canonical()

        # Root (no profile) — allow everything
        if not canonical:
            return False, None, None

        # Check governance files
        for gov in GOVERNANCE_PATHS:
            if target_path == gov.resolve():
                return True, f"SCOPE VIOLATION: {target_path.name} is a governance file", None

        # Check read-only shared dirs
        for ro_dir in READ_ONLY_DIRS:
            if str(target_path).startswith(str(ro_dir.resolve())):
                return True, f"SCOPE VIOLATION: {ro_dir.name} is read-only", None

        # Get agent's own space
        own_space = AGENT_SPACES.get(canonical)
        if not own_space:
            return False, None, None

        own_space_path = Path(own_space).resolve()
        is_own = str(target_path).startswith(str(own_space_path))

        if is_own:
            return False, None, None  # Allowed

        # Outside own space — check identity file protection
        target_name = target_path.name
        is_identity = any(p.search(target_name) for p in IDENTITY_PATTERNS)

        if is_identity:
            # Curator exception for MEMORY.md
            if canonical == CURATOR and "MEMORY" in target_name:
                return False, None, None
            return True, (
                f"SCOPE VIOLATION: {target_name} is an identity file outside your agent-space. "
                f"You may only write inside: {own_space}"
            ), None

        # Cross-agent non-identity write
        # Curator exception for MEMORY.md
        if canonical == CURATOR and "MEMORY" in target_name:
            return False, None, None

        for other_canonical, other_space in AGENT_SPACES.items():
            if other_canonical == canonical:
                continue
            if str(target_path).startswith(str(Path(other_space).resolve())):
                return True, (
                    f"SCOPE VIOLATION: {target} is inside {other_canonical}'s agent-space. "
                    f"You may only write inside: {own_space}"
                ), None

        return False, None, None
