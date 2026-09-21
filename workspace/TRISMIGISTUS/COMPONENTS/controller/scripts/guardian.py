#!/usr/bin/env python3
"""
Guardian — Agent Scope Enforcer

Validates write operations against agent scope rules.
Called by agent hooks or can be used as a standalone validator.

Usage:
    python3 guardian.py check-write <agent_canonical> <target_path>
    python3 guardian.py check-read <agent_canonical> <target_path>
    python3 guardian.py validate-all  # check all agents
    python3 guardian.py lockdown      # chmod identity files read-only
    
Returns:
    0 = allowed
    1 = blocked (with reason to stderr)
"""

import json
import os
import sys
import stat
from pathlib import Path
from datetime import datetime, timezone

BASE = Path("/root/MW_CENTRAL")
MATRIX = BASE / "ANDROMALIUS/MATRIX"
CONTROLLER = BASE / "ANDROMALIUS/TRISMIGISTUS/COMPONENTS/controller"
VIOLATION_LOG = CONTROLLER / "receipts/scope-violations.jsonl"

# Identity files that cannot be written by other agents
IDENTITY_SUFFIXES = ["SOUL.md", "SCOPE.md", "MEMORY.md", "config.yaml", "state.md"]

# Governance files no agent may write
GOVERNANCE_FILES = [
    BASE / "AGENTS.md",
    BASE / ".hermes.md",
    BASE / "ANDROMALIUS/.hermes.md",
]


def load_authority():
    with open(MATRIX / "naming-authority.json") as f:
        return json.load(f)["agents"]


def resolve_name(variant, agents):
    """Resolve any name variant to canonical."""
    if variant in agents:
        return variant
    cleaned = variant.replace("AGENT_", "").replace("_TRIS", "")
    if cleaned in agents:
        return cleaned
    norm = cleaned.replace("_", "").replace("-", "").lower()
    for canonical in agents:
        if canonical.replace("_", "").lower() == norm:
            return canonical
    return None


def get_agent_space(canonical, agents):
    """Get absolute path to agent's agent-space."""
    as_path = agents[canonical]["paths"]["agent_space"]
    if as_path is None:
        return None
    if as_path.startswith("ANDROMALIUS/"):
        return BASE / as_path
    return Path(as_path)


def is_identity_file(path):
    """Check if path is an identity file."""
    name = Path(path).name
    return any(name.endswith(suf) for suf in IDENTITY_SUFFIXES)


def is_governance_file(path):
    """Check if path is a governance file."""
    resolved = Path(path).resolve()
    return any(resolved == gf.resolve() for gf in GOVERNANCE_FILES)


def check_write(agent_canonical, target_path):
    """Check if agent can write to target_path. Returns (allowed, reason)."""
    agents = load_authority()
    canonical = resolve_name(agent_canonical, agents)
    
    if not canonical:
        return False, f"Unknown agent: {agent_canonical}"
    
    target = Path(target_path).resolve()
    
    # Check governance files first
    if is_governance_file(target):
        return False, f"BLOCKED: {target.name} is a governance file — no agent may write"
    
    # Get agent's own space
    own_space = get_agent_space(canonical, agents)
    
    # Check if target is within own agent-space
    if own_space and target.is_relative_to(own_space):
        # Writing to own space — allowed
        # But check if it's an identity file being overwritten by non-owner
        # (this shouldn't happen since it IS the owner)
        return True, "OK: Writing to own agent-space"
    
    # Target is outside own space
    # Check if it's another agent's identity file
    if is_identity_file(target):
        # Exception: MEMORY_CURATOR can write MEMORY.md in all agent-spaces
        if canonical == "MEMORY_CURATOR" and target.name.endswith("MEMORY.md"):
            return True, "OK: Curator managing agent memory (special scope)"
        return False, f"BLOCKED: {target.name} is an identity file outside your scope"
    
    # Check if it's inside another agent's agent-space
    for other_canonical, other_entry in agents.items():
        if other_canonical == canonical:
            continue
        other_space = get_agent_space(other_canonical, agents)
        if other_space and target.is_relative_to(other_space):
            return False, f"BLOCKED: {target} is inside {other_canonical}'s agent-space"
    
    # Writing to shared area (MATRIX, KNOWLEDGE_LIBRARY, etc.)
    # Only allow if explicitly in scope
    shared_allowed = [
        BASE / "ANDROMALIUS/MATRIX",
        BASE / "ANDROMALIUS/KNOWLEDGE_LIBRARY",
    ]
    for shared in shared_allowed:
        if target.is_relative_to(shared):
            return False, f"BLOCKED: {shared.name} is read-only for agents"
    
    return False, f"BLOCKED: {target} is outside your scope"


def check_read(agent_canonical, target_path):
    """Check if agent can read target_path."""
    target = Path(target_path).resolve()
    
    # Block secret files
    secret_names = {".env", "auth.json", "credentials.json", "secrets.json"}
    if target.name in secret_names:
        return False, f"BLOCKED: {target.name} is a secret file"
    
    # Block other agents' config.yaml (contains provider settings)
    if target.name == "config.yaml":
        agents = load_authority()
        for canonical, entry in agents.items():
            prof = entry["paths"]["profile"]
            if prof:
                if prof.startswith("~/"):
                    prof_dir = Path.home() / prof[2:]
                elif prof.startswith("ANDROMALIUS/"):
                    prof_dir = BASE / prof
                else:
                    prof_dir = Path(prof)
                if target.parent.resolve() == prof_dir.resolve():
                    # It's a profile config — allow read but flag
                    return True, "WARN: Reading another agent's profile config (allowed, logged)"
    
    return True, "OK"


def log_violation(agent, action, target, reason):
    """Log scope violation."""
    VIOLATION_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent": agent,
        "action": action,
        "target": str(target),
        "reason": reason,
    }
    with open(VIOLATION_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


def lockdown():
    """Set identity files to read-only (chmod 644) for cross-agent protection."""
    agents = load_authority()
    protected = 0
    
    for canonical, entry in agents.items():
        as_path = entry["paths"]["agent_space"]
        if not as_path:
            continue
        if as_path.startswith("ANDROMALIUS/"):
            full = BASE / as_path
        else:
            full = Path(as_path)
        
        if not full.exists():
            continue
        
        for f in full.iterdir():
            if f.is_file() and any(f.name.endswith(suf) for suf in IDENTITY_SUFFIXES):
                # Set to owner read/write, group/others read-only
                os.chmod(f, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
                protected += 1
    
    print(f"Lockdown complete: {protected} identity files set to 644")
    return protected


def validate_all():
    """Validate all agents have proper scope config."""
    agents = load_authority()
    issues = []
    
    for canonical, entry in agents.items():
        prof_path = entry["paths"]["profile"]
        if not prof_path:
            issues.append(f"{canonical}: no profile")
            continue
        
        if prof_path.startswith("~/"):
            full_prof = Path.home() / prof_path[2:]
        else:
            full_prof = Path(prof_path)
        
        config = full_prof / "config.yaml"
        if config.exists():
            text = config.read_text()
            if "scope:" not in text:
                issues.append(f"{canonical}: profile missing scope config")
            if "allowed_writes" not in text:
                issues.append(f"{canonical}: profile missing allowed_writes")
    
    if issues:
        print(f"Validation issues ({len(issues)}):")
        for i in issues:
            print(f"  ⚠️ {i}")
    else:
        print("✅ All agents have proper scope configuration")
    
    return len(issues) == 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "check-write":
        if len(sys.argv) < 4:
            print("Usage: guardian.py check-write <agent> <target_path>")
            sys.exit(1)
        allowed, reason = check_write(sys.argv[2], sys.argv[3])
        print(reason)
        if not allowed:
            log_violation(sys.argv[2], "write", sys.argv[3], reason)
        sys.exit(0 if allowed else 1)
    
    elif command == "check-read":
        if len(sys.argv) < 4:
            print("Usage: guardian.py check-read <agent> <target_path>")
            sys.exit(1)
        allowed, reason = check_read(sys.argv[2], sys.argv[3])
        print(reason)
        sys.exit(0 if allowed else 1)
    
    elif command == "lockdown":
        lockdown()
    
    elif command == "validate-all":
        ok = validate_all()
        sys.exit(0 if ok else 1)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
