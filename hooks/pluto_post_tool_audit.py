#!/usr/bin/env python3
"""Post-tool audit hook for Pluto/Lane A activity.

Reads Hermes shell-hook JSON on stdin and appends a redacted JSONL event to
Pluto hook logs. Observer only: never blocks or modifies tool results.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path("/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX")
LOG = ROOT / "Y-MINDWAVE" / "H3_SYSTEM" / "07_HOOKS" / "02_LOGS" / "post_tool_audit.jsonl"
SENSITIVE_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|password|secret|authorization)\s*[:=]\s*[^\s,;}]+"),
]


def scrub(value: Any, limit: int = 1200) -> Any:
    if isinstance(value, dict):
        return {str(k): scrub(v, limit=limit) for k, v in value.items() if str(k).lower() not in {"authorization", "api_key", "token", "password", "secret"}}
    if isinstance(value, list):
        return [scrub(v, limit=limit) for v in value[:50]]
    if isinstance(value, str):
        out = value[:limit]
        for pat in SENSITIVE_PATTERNS:
            out = pat.sub(lambda m: m.group(1) + "=[REDACTED]", out)
        return out
    return value


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except Exception as e:
        payload = {"parse_error": str(e), "raw_sha256": hashlib.sha256(raw.encode("utf-8", errors="replace")).hexdigest()}

    args = payload.get("tool_input") or payload.get("args") or {}
    text = json.dumps(args, ensure_ascii=False, default=str)
    pluto_related = "/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX" in text or "D:/MW_CENTRAL/TRIANGULUM/HELIOS/NYX" in text or "D:\\MW_CENTRAL\\TRIANGULUM\\HELIOS\\NYX" in text or "ANDROMALIUS" in text
    lane_related = "Lane A" in text or "LANE_A" in text or "03_LANE_A" in text

    entry = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "event": payload.get("hook_event_name"),
        "tool_name": payload.get("tool_name"),
        "session_id": payload.get("session_id"),
        "cwd": payload.get("cwd"),
        "status": (payload.get("extra") or {}).get("status"),
        "pluto_related": pluto_related,
        "lane_related": lane_related,
        "tool_input": scrub(args),
        "extra_summary": scrub(payload.get("extra") or {}, limit=500),
    }
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
