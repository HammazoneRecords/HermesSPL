#!/usr/bin/env python3
"""Guard session reads and writes at the pre-tool boundary.

The hook is deliberately deny-by-default for session data.  The caller is
identified by ``HERMES_PROFILE`` (or ``actor_profile`` in the tool input), and
session metadata may carry ``owner``/``agent_id``.  Explicit grants can be
provided with ``SESSION_ACCESS_POLICY`` (a JSON file) or the fork-local
``policy/session_access_policy.json``.

Public metadata is allowed without a session grant; transcript/state/content
access is not.  Curator access is never implicit: the policy must name the
curator and enable the requested read/write permission.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_POLICY = ROOT / "policy" / "session_access_policy.json"
READ_TOOLS = {"read_session", "session_read", "get_session", "read_transcript", "session_export"}
WRITE_TOOLS = {"write_session", "session_write", "update_session", "delete_session", "append_session"}
SESSION_KEYS = ("session_id", "target_session_id", "session", "target")


def _policy() -> dict[str, Any]:
    path = Path(os.environ.get("SESSION_ACCESS_POLICY", str(DEFAULT_POLICY)))
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError, TypeError):
        return {}


def _actor(tool_input: dict[str, Any]) -> str:
    return str(tool_input.get("actor_profile") or tool_input.get("agent_id") or os.environ.get("HERMES_PROFILE", "")).strip().lower()


def _target(tool_input: dict[str, Any]) -> dict[str, Any] | None:
    raw = tool_input.get("session_metadata") or tool_input.get("target_session")
    if isinstance(raw, dict):
        return raw
    sid = next((tool_input[k] for k in SESSION_KEYS if tool_input.get(k) is not None), None)
    if sid is None:
        return None
    return {"session_id": str(sid), "owner": tool_input.get("session_owner") or tool_input.get("owner")}


def _is_public_metadata(tool_input: dict[str, Any], target: dict[str, Any] | None) -> bool:
    scope = str(tool_input.get("access_scope") or tool_input.get("session_access") or "").lower()
    operation = str(tool_input.get("operation") or tool_input.get("data_kind") or "").lower()
    return scope in {"public", "public_metadata", "metadata"} or operation in {"metadata", "public_metadata"} or bool(target and target.get("public_metadata") is True)


def _allowed_grant(policy: dict[str, Any], actor: str, target_id: str, access: str) -> bool:
    shared = policy.get("shared_sessions", {})
    if isinstance(shared, dict):
        entry = shared.get(target_id, {})
        if isinstance(entry, dict):
            allowed = entry.get(access, entry.get("read_write" if access == "write" else "read", []))
            if isinstance(allowed, str):
                allowed = [allowed]
            if isinstance(allowed, list) and actor in {str(x).lower() for x in allowed}:
                return True
    grants = policy.get("grants", [])
    if isinstance(grants, list):
        return any(isinstance(g, dict) and str(g.get("actor", "")).lower() == actor and str(g.get("session", g.get("session_id", ""))) == target_id and access in g.get("permissions", []) for g in grants)
    return False


def _curator_allowed(policy: dict[str, Any], actor: str, access: str) -> bool:
    curators = {str(x).lower() for x in policy.get("curator_profiles", [])} if isinstance(policy.get("curator_profiles", []), list) else set()
    permissions = policy.get("curator_permissions", [])
    return actor in curators and access in permissions


def enforce(tool_name: str, tool_input: dict[str, Any]) -> dict[str, Any]:
    """Return a JSON-compatible allow/block decision for one tool call."""
    if tool_name not in READ_TOOLS | WRITE_TOOLS:
        return {"action": "allow", "reason": "not a session access tool"}
    if not isinstance(tool_input, dict):
        return {"action": "block", "reason": "invalid session tool input"}
    target = _target(tool_input)
    if target is None:
        return {"action": "block", "reason": "session target is required"}
    access = "read" if tool_name in READ_TOOLS else "write"
    if access == "read" and _is_public_metadata(tool_input, target):
        return {"action": "allow", "reason": "public session metadata"}
    actor = _actor(tool_input)
    owner = str(target.get("owner") or target.get("agent_id") or "").strip().lower()
    target_id = str(target.get("session_id") or target.get("id") or "")
    policy = _policy()
    if actor and owner and actor == owner:
        return {"action": "allow", "reason": "agent owns session"}
    if target_id and _allowed_grant(policy, actor, target_id, access):
        return {"action": "allow", "reason": "explicit shared-session grant"}
    if target_id and _curator_allowed(policy, actor, access):
        return {"action": "allow", "reason": "policy-authorized curator access"}
    return {"action": "block", "reason": f"unauthorized cross-agent session {access}"}


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        result = enforce(str(payload.get("tool_name", "")), payload.get("tool_input") or payload.get("args") or {})
    except (json.JSONDecodeError, TypeError, AttributeError):
        result = {"action": "block", "reason": "invalid JSON hook input"}
    print(json.dumps(result, ensure_ascii=False))
    return 2 if result["action"] == "block" else 0


if __name__ == "__main__":
    raise SystemExit(main())
