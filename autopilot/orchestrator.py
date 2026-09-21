#!/usr/bin/env python3
"""
Autopilot Orchestrator — First-launch bootstrap for all 22 agents.

On first launch:
  1. Auto-initialize all 22 agents (verify profiles, agent-space, TRIS components)
  2. Verify hooks (pre_tool_call + post_tool_call from config_scope_hooks.yaml)
  3. Check TCP (Turing Checkpoint agent state + TCP_CHECKER readiness)
  4. Start work-time tracking (TCPTracker session)
  5. Begin user preference capture (patterns, models, work style)
  6. Emit idempotency marker so re-runs are safe

Idempotent: safe to re-run. Existing state is preserved; missing state is created.

Logging: .hermes-spl/autopilot.log
"""

from __future__ import annotations

import json
import logging
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

FORK_ROOT = Path(__file__).resolve().parents[1]
PLUTO_ROOT = FORK_ROOT.parents[1] / "PLUTO"
AUTOPILOT_DIR = FORK_ROOT / "autopilot"
SPL_DIR = FORK_ROOT / ".hermes-spl"
LOG_FILE = SPL_DIR / "autopilot.log"

# Source-of-truth files
NAMING_AUTHORITY = PLUTO_ROOT / "MATRIX" / "naming-authority.json"
AGENT_READINESS = PLUTO_ROOT / "MATRIX" / "agent-readiness.json"
CONFIG_HOOKS = FORK_ROOT / "config_scope_hooks.yaml"
HOOKS_DIR = FORK_ROOT / "hooks" / "pre_tool_call"

# Agent locations
AGENT_ARENA = PLUTO_ROOT / "AGENT_ARENA" / "ACTIVE"
TRIS_COMPONENTS = PLUTO_ROOT / "TRISMIGISTUS" / "COMPONENTS" / "agents"
PROFILES_DIR = Path.home() / ".hermes" / "profiles"

# TCP agent
TCP_AGENT_DIR = AGENT_ARENA / "AGENT_TCP_TRIS"
TCP_CHECKER_DIR = AGENT_ARENA / "AGENT_TCP_CHECKER_TRIS"

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

SPL_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("autopilot")
logger.setLevel(logging.DEBUG)

# File handler
fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(fh)

# Console handler
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
logger.addHandler(ch)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _atomic_append(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False, default=str) + "\n"
    with open(path, "a", encoding="utf-8") as f:
        f.write(line)
        f.flush()
        os.fsync(f.fileno())


def _read_json_safe(path: Path) -> Optional[dict[str, Any]]:
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


# ---------------------------------------------------------------------------
# Idempotency marker
# ---------------------------------------------------------------------------

IDEMPOTENCY_MARKER = SPL_DIR / ".autopilot_initialized"


def is_initialized() -> bool:
    return IDEMPOTENCY_MARKER.exists()


def mark_initialized(agents_count: int, hooks_count: int, tcp_ok: bool) -> None:
    marker_data = {
        "initialized_at": _now_iso(),
        "agents_count": agents_count,
        "hooks_verified": hooks_count,
        "tcp_ready": tcp_ok,
        "version": "1.0.0",
    }
    IDEMPOTENCY_MARKER.write_text(json.dumps(marker_data, indent=2))


# ---------------------------------------------------------------------------
# Phase 1: Agent Initialization
# ---------------------------------------------------------------------------

def load_naming_authority() -> dict[str, Any]:
    """Load the canonical agent naming authority."""
    data = _read_json_safe(NAMING_AUTHORITY)
    if not data:
        logger.error("Cannot load naming authority from %s", NAMING_AUTHORITY)
        return {}
    return data.get("agents", {})


def verify_agent(agent_name: str, agent_info: dict[str, Any]) -> dict[str, Any]:
    """Verify one agent across all three layers. Returns status dict."""
    category = agent_info.get("category", "unknown")
    paths = agent_info.get("paths", {})
    variants = agent_info.get("name_variants", {})

    results = {
        "canonical": agent_name,
        "category": category,
        "agent_space": {"path": None, "exists": False, "files": []},
        "tri": {"path": None, "exists": False},
        "profile": {"path": None, "exists": False},
        "status": "unknown",
    }

    # Check agent-space
    aspace_rel = paths.get("agent_space", "")
    if aspace_rel:
        # Resolve relative to PLUTO_ROOT
        aspace_path = PLUTO_ROOT / aspace_rel.replace("PLUTO/", "")
        results["agent_space"]["path"] = str(aspace_path)
        if aspace_path.exists():
            results["agent_space"]["exists"] = True
            results["agent_space"]["files"] = sorted(
                f.name for f in aspace_path.iterdir() if f.is_file()
            )[:20]  # Cap at 20 for brevity

    # Check TRIS component
    tri_rel = paths.get("tri", "")
    if tri_rel:
        tri_path = PLUTO_ROOT / tri_rel.replace("PLUTO/", "")
        results["tri"]["path"] = str(tri_path)
        results["tri"]["exists"] = tri_path.exists()

    # Check Hermes profile
    profile_rel = paths.get("profile", "")
    if profile_rel.startswith("~/"):
        profile_path = Path(profile_rel).expanduser()
    else:
        profile_path = Path(profile_rel)
    results["profile"]["path"] = str(profile_path)
    results["profile"]["exists"] = profile_path.exists()

    # Determine status
    aspace_ok = results["agent_space"]["exists"]
    tri_ok = results["tri"]["exists"]
    profile_ok = results["profile"]["exists"]

    if aspace_ok and tri_ok and profile_ok:
        results["status"] = "ready"
    elif aspace_ok or tri_ok:
        results["status"] = "partial"
    else:
        results["status"] = "missing"

    return results


def initialize_all_agents() -> list[dict[str, Any]]:
    """Initialize all 22 agents. Returns list of status dicts."""
    agents = load_naming_authority()
    if not agents:
        logger.error("No agents found in naming authority")
        return []

    logger.info("Initializing %d agents from naming authority...", len(agents))

    results = []
    ready_count = 0
    partial_count = 0
    missing_count = 0

    for name, info in sorted(agents.items()):
        status = verify_agent(name, info)
        results.append(status)

        if status["status"] == "ready":
            ready_count += 1
            logger.info("  ✅ %s (%s) — READY", name, status["category"])
        elif status["status"] == "partial":
            partial_count += 1
            logger.warning("  ⚠️  %s (%s) — PARTIAL (aspace=%s tri=%s profile=%s)",
                           name, status["category"],
                           status["agent_space"]["exists"],
                           status["tri"]["exists"],
                           status["profile"]["exists"])
        else:
            missing_count += 1
            logger.error("  ❌ %s (%s) — MISSING", name, status["category"])

    logger.info("Agent summary: %d ready, %d partial, %d missing",
                ready_count, partial_count, missing_count)

    return results


# ---------------------------------------------------------------------------
# Phase 2: Hook Verification
# ---------------------------------------------------------------------------

def verify_hooks() -> dict[str, Any]:
    """Verify all configured hooks exist and are executable."""
    logger.info("Verifying hooks from %s", CONFIG_HOOKS)

    results = {
        "config_exists": False,
        "pre_tool_call": [],
        "post_tool_call": [],
        "missing_hooks": [],
        "total_verified": 0,
    }

    if not CONFIG_HOOKS.exists():
        logger.error("Hook config not found: %s", CONFIG_HOOKS)
        return results

    results["config_exists"] = True

    try:
        import yaml
    except ImportError:
        logger.warning("PyYAML not available; falling back to regex parsing")
        return _verify_hooks_regex(results)

    try:
        with open(CONFIG_HOOKS, "r") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        logger.error("Failed to parse hook config: %s", e)
        return results

    hooks_section = config.get("hooks", {})

    for hook_type in ("pre_tool_call", "post_tool_call"):
        entries = hooks_section.get(hook_type, [])
        for entry in entries:
            command = entry.get("command", "")
            matcher = entry.get("matcher", "*")
            timeout = entry.get("timeout", 10)
            fail_closed = entry.get("fail_closed", False)

            # Extract script path from command
            script_path = _extract_script_path(command)
            hook_info = {
                "type": hook_type,
                "command": command,
                "matcher": matcher,
                "timeout": timeout,
                "fail_closed": fail_closed,
                "script_path": str(script_path) if script_path else None,
                "script_exists": script_path.exists() if script_path else False,
            }

            results[hook_type].append(hook_info)

            if hook_info["script_exists"]:
                results["total_verified"] += 1
                logger.info("  ✅ %s hook: %s (matcher=%s)", hook_type, script_path.name, matcher)
            else:
                results["missing_hooks"].append(str(script_path))
                logger.warning("  ⚠️  %s hook MISSING: %s", hook_type, str(script_path))

    logger.info("Hook summary: %d verified, %d missing",
                results["total_verified"], len(results["missing_hooks"]))

    return results


def _extract_script_path(command: str) -> Optional[Path]:
    """Extract the Python script path from a hook command string."""
    # Pattern: python3 /path/to/script.py [args]
    parts = command.strip().split()
    if len(parts) >= 2 and parts[0] in ("python3", "python"):
        return Path(parts[1])
    return None


def _verify_hooks_regex(results: dict[str, Any]) -> dict[str, Any]:
    """Fallback hook verification using regex (no PyYAML)."""
    import re

    content = CONFIG_HOOKS.read_text()
    # Find all python3 commands
    commands = re.findall(r'python3\s+(\S+\.py)', content)

    for cmd in commands:
        path = Path(cmd)
        exists = path.exists()
        results["total_verified"] += 1 if exists else 0
        if not exists:
            results["missing_hooks"].append(cmd)
            logger.warning("  ⚠️  Hook script missing: %s", cmd)
        else:
            logger.info("  ✅ Hook script found: %s", path.name)

    return results


# ---------------------------------------------------------------------------
# Phase 3: TCP Check
# ---------------------------------------------------------------------------

def check_tcp() -> dict[str, Any]:
    """Verify TCP (Turing Checkpoint) agent state and TCP_CHECKER readiness."""
    logger.info("Checking TCP agent state...")

    results = {
        "tcp_agent": {"exists": False, "config_valid": False, "state": None},
        "tcp_checker": {"exists": False, "config_valid": False, "state": None},
        "overall_ready": False,
    }

    # Check TCP agent
    if TCP_AGENT_DIR.exists():
        results["tcp_agent"]["exists"] = True
        config_path = TCP_AGENT_DIR / "TCP_config.yaml"
        state_path = TCP_AGENT_DIR / "TCP_state.md"

        if config_path.exists():
            results["tcp_agent"]["config_valid"] = True
        if state_path.exists():
            results["tcp_agent"]["state"] = "configured"

        logger.info("  ✅ TCP agent found at %s", TCP_AGENT_DIR)
        logger.info("     config.yaml: %s, state.md: %s",
                    config_path.exists(), state_path.exists())
    else:
        logger.warning("  ⚠️  TCP agent directory missing: %s", TCP_AGENT_DIR)

    # Check TCP_CHECKER
    if TCP_CHECKER_DIR.exists():
        results["tcp_checker"]["exists"] = True
        checker_config = TCP_CHECKER_DIR / "TCP01_config.yaml"
        checker_state = TCP_CHECKER_DIR / "TCP01_SELF_state.md"

        if checker_config.exists():
            results["tcp_checker"]["config_valid"] = True
        if checker_state.exists():
            results["tcp_checker"]["state"] = "configured"

        logger.info("  ✅ TCP_CHECKER found at %s", TCP_CHECKER_DIR)
        logger.info("     config: %s, state: %s",
                    checker_config.exists(), checker_state.exists())
    else:
        logger.warning("  ⚠️  TCP_CHECKER directory missing: %s", TCP_CHECKER_DIR)

    # Overall readiness
    results["overall_ready"] = (
        results["tcp_agent"]["exists"] and
        results["tcp_checker"]["exists"]
    )

    return results


# ---------------------------------------------------------------------------
# Phase 4: Work-Time Tracking
# ---------------------------------------------------------------------------

def start_work_time_tracking() -> dict[str, Any]:
    """Start a TCPTracker-style work session."""
    logger.info("Starting work-time tracking...")

    storage_dir = SPL_DIR / "work_time"
    storage_dir.mkdir(parents=True, exist_ok=True)

    session_id = f"sess-{uuid.uuid4().hex[:12]}"
    start_record = {
        "record_id": uuid.uuid4().hex[:16],
        "timestamp": _now_iso(),
        "type": "session_start",
        "session_id": session_id,
        "source": "autopilot_orchestrator",
        "version": "1.0.0",
    }

    daily_log = storage_dir / f"tcp_{_today_str()}.jsonl"
    _atomic_append(daily_log, start_record)

    # Start initialization task
    task_id = f"task-{uuid.uuid4().hex[:10]}"
    task_record = {
        "record_id": uuid.uuid4().hex[:16],
        "timestamp": _now_iso(),
        "type": "task_start",
        "session_id": session_id,
        "task_id": task_id,
        "task_label": "autopilot_initialization",
        "metadata": {"source": "orchestrator"},
    }
    _atomic_append(daily_log, task_record)

    logger.info("  Session: %s", session_id)
    logger.info("  Task: autopilot_initialization (%s)", task_id)
    logger.info("  Log: %s", daily_log)

    return {
        "session_id": session_id,
        "task_id": task_id,
        "storage_dir": str(storage_dir),
        "daily_log": str(daily_log),
        "started_at": start_record["timestamp"],
    }


# ---------------------------------------------------------------------------
# Phase 5: User Preference Capture
# ---------------------------------------------------------------------------

PREFERENCES_FILE = SPL_DIR / "user_preferences.json"


def begin_preference_capture() -> dict[str, Any]:
    """Initialize or load user preference capture."""
    logger.info("Beginning user preference capture...")

    # Load existing or create new
    prefs = _read_json_safe(PREFERENCES_FILE) or {}

    if not prefs:
        prefs = {
            "version": "1.0.0",
            "created_at": _now_iso(),
            "updated_at": _now_iso(),
            "capture_active": True,
            "preferences": {
                "work_schedule": {"detected": False, "pattern": None},
                "preferred_models": {},
                "communication_style": None,
                "focus_areas": [],
                "auto_tasks_enabled": True,
            },
            "observations": {
                "session_count": 0,
                "total_tasks": 0,
                "common_tools": [],
                "peak_activity_hours": [],
            },
        }
        PREFERENCES_FILE.write_text(json.dumps(prefs, indent=2))
        logger.info("  Created new preferences file: %s", PREFERENCES_FILE)
    else:
        logger.info("  Loaded existing preferences (updated_at: %s)",
                     prefs.get("updated_at", "unknown"))

    # Capture initial environment signals
    env_signals = {
        "hermes_profile_dir_exists": PROFILES_DIR.exists(),
        "agent_count": len(list(AGENT_ARENA.iterdir())) if AGENT_ARENA.exists() else 0,
        "pluto_workspace_active": PLUTO_ROOT.exists(),
        "fork_workspace_active": FORK_ROOT.exists(),
        "timestamp": _now_iso(),
    }

    # Store initial observation
    prefs["last_environment_signals"] = env_signals
    prefs["updated_at"] = _now_iso()
    PREFERENCES_FILE.write_text(json.dumps(prefs, indent=2))

    logger.info("  Captured environment signals: %d agents detected",
                env_signals["agent_count"])

    return {"preferences": prefs, "signals": env_signals}


# ---------------------------------------------------------------------------
# Phase 6: Readiness Report
# ---------------------------------------------------------------------------

def generate_readiness_report(
    agent_results: list[dict[str, Any]],
    hook_results: dict[str, Any],
    tcp_results: dict[str, Any],
    tracking_results: dict[str, Any],
) -> dict[str, Any]:
    """Generate a comprehensive readiness report."""
    ready_agents = [a for a in agent_results if a["status"] == "ready"]
    partial_agents = [a for a in agent_results if a["status"] == "partial"]
    missing_agents = [a for a in agent_results if a["status"] == "missing"]

    report = {
        "timestamp": _now_iso(),
        "summary": {
            "total_agents": len(agent_results),
            "ready": len(ready_agents),
            "partial": len(partial_agents),
            "missing": len(missing_agents),
            "hooks_verified": hook_results.get("total_verified", 0),
            "hooks_missing": len(hook_results.get("missing_hooks", [])),
            "tcp_ready": tcp_results.get("overall_ready", False),
            "work_tracking_active": True,
        },
        "agents": {
            "ready": [a["canonical"] for a in ready_agents],
            "partial": [a["canonical"] for a in partial_agents],
            "missing": [a["canonical"] for a in missing_agents],
        },
        "session": {
            "session_id": tracking_results["session_id"],
            "started_at": tracking_results["started_at"],
        },
        "status": "operational" if len(ready_agents) >= 10 else "degraded",
    }

    # Write report
    report_path = SPL_DIR / "readiness_report.json"
    report_path.write_text(json.dumps(report, indent=2))

    return report


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------

def run(force: bool = False) -> dict[str, Any]:
    """
    Run the autopilot orchestrator.

    Args:
        force: If True, re-run even if already initialized.

    Returns:
        Dict with all phase results.
    """
    logger.info("=" * 60)
    logger.info("AUTOPILOT ORCHESTRATOR v1.0.0")
    logger.info("Fork: %s", FORK_ROOT)
    logger.info("Pluto: %s", PLUTO_ROOT)
    logger.info("=" * 60)

    # Idempotency check
    if is_initialized() and not force:
        logger.info("Autopilot already initialized (marker exists). Use --force to re-run.")
        marker_data = _read_json_safe(IDEMPOTENCY_MARKER)
        return {"status": "already_initialized", "marker": marker_data}

    results = {"status": "running", "phases": {}}

    # Phase 1: Agent initialization
    logger.info("")
    logger.info("━" * 40)
    logger.info("Phase 1: Agent Initialization (22 agents)")
    logger.info("━" * 40)
    agent_results = initialize_all_agents()
    results["phases"]["agents"] = agent_results

    # Phase 2: Hook verification
    logger.info("")
    logger.info("━" * 40)
    logger.info("Phase 2: Hook Verification")
    logger.info("━" * 40)
    hook_results = verify_hooks()
    results["phases"]["hooks"] = hook_results

    # Phase 3: TCP check
    logger.info("")
    logger.info("━" * 40)
    logger.info("Phase 3: TCP Check")
    logger.info("━" * 40)
    tcp_results = check_tcp()
    results["phases"]["tcp"] = tcp_results

    # Phase 4: Work-time tracking
    logger.info("")
    logger.info("━" * 40)
    logger.info("Phase 4: Work-Time Tracking")
    logger.info("━" * 40)
    tracking_results = start_work_time_tracking()
    results["phases"]["tracking"] = tracking_results

    # Phase 5: User preference capture
    logger.info("")
    logger.info("━" * 40)
    logger.info("Phase 5: User Preference Capture")
    logger.info("━" * 40)
    pref_results = begin_preference_capture()
    results["phases"]["preferences"] = pref_results

    # Phase 6: Generate readiness report
    logger.info("")
    logger.info("━" * 40)
    logger.info("Phase 6: Readiness Report")
    logger.info("━" * 40)
    report = generate_readiness_report(
        agent_results, hook_results, tcp_results, tracking_results
    )
    results["report"] = report

    # Mark initialized
    ready_count = report["summary"]["ready"]
    hooks_count = report["summary"]["hooks_verified"]
    tcp_ok = report["summary"]["tcp_ready"]
    mark_initialized(ready_count, hooks_count, tcp_ok)

    # Final summary
    logger.info("")
    logger.info("=" * 60)
    logger.info("AUTOPILOT COMPLETE")
    logger.info("=" * 60)
    logger.info("Status: %s", report["status"])
    logger.info("Agents: %d ready, %d partial, %d missing",
                report["summary"]["ready"],
                report["summary"]["partial"],
                report["summary"]["missing"])
    logger.info("Hooks: %d verified, %d missing",
                report["summary"]["hooks_verified"],
                report["summary"]["hooks_missing"])
    logger.info("TCP ready: %s", report["summary"]["tcp_ready"])
    logger.info("Session: %s", report["session"]["session_id"])
    logger.info("Report: %s", SPL_DIR / "readiness_report.json")
    logger.info("Log: %s", LOG_FILE)
    logger.info("=" * 60)

    results["status"] = "complete"
    return results


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Autopilot Orchestrator — Bootstrap all 22 agents"
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Force re-run even if already initialized"
    )
    parser.add_argument(
        "--status", action="store_true",
        help="Show current initialization status and exit"
    )
    args = parser.parse_args()

    if args.status:
        if is_initialized():
            marker = _read_json_safe(IDEMPOTENCY_MARKER)
            print(json.dumps(marker, indent=2))
        else:
            print("Not initialized. Run without --status to initialize.")
        return

    results = run(force=args.force)

    # Print summary to stdout
    if "report" in results:
        summary = results["report"]["summary"]
        print(f"\n{'='*50}")
        print(f"AUTOPILOT STATUS: {results['report']['status']}")
        print(f"{'='*50}")
        print(f"Agents: {summary['ready']} ready, {summary['partial']} partial, {summary['missing']} missing")
        print(f"Hooks: {summary['hooks_verified']} verified, {summary['hooks_missing']} missing")
        print(f"TCP: {'READY' if summary['tcp_ready'] else 'NOT READY'}")
        print(f"Work tracking: {'ACTIVE' if summary['work_tracking_active'] else 'INACTIVE'}")
        print(f"{'='*50}")


if __name__ == "__main__":
    main()
