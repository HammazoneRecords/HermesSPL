#!/usr/bin/env python3
"""Pre-tool guard hook for Pluto migration safety.

Blocks obvious destructive commands or file operations under ANDROMALIUS unless the
payload carries an explicit approval marker. Enforces filename conventions:
no spaces in filenames, use '-' or '_' instead.

Designed for Hermes shell hooks on pre_tool_call with fail_closed=true.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ANDROMALIUS_MARKERS = ["/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX", "D:/MW_CENTRAL/TRIANGULUM/HELIOS/NYX", "D:\\MW_CENTRAL\\TRIANGULUM\\HELIOS\\NYX", "ANDROMALIUS"]
APPROVAL_MARKERS = ["ANDROMALIUS_DESTRUCTIVE_APPROVED", "hash-before-after-approved"]
FILENAME_APPROVAL_MARKER = "ANDROMALIUS_FILENAME_VALIDATED"

# Denylist for filenames (basename component, case-insensitive)
FILENAME_DENY_PATTERNS = [
    re.compile(r"\s"),                               # any whitespace / spaces
    re.compile(r"[^a-zA-Z0-9._\-/]"),                # allow letters, digits, dot, hyphen, underscore, slash
]

# Allowed extensions for text files; binary docs handled by Hermes schema layer
FILENAME_REQUIRED_EXTENSION = re.compile(r"\.[a-zA-Z]{1,10}$")

DESTRUCTIVE_PATTERNS = [
    re.compile(r"\brm\s+-rf\b", re.I),
    re.compile(r"\brm\s+-r\b", re.I),
    re.compile(r"\bdel\b", re.I),
    re.compile(r"\brmdir\b", re.I),
    re.compile(r"\bmove\b", re.I),
    re.compile(r"\bmv\b", re.I),
    re.compile(r"\bRemove-Item\b", re.I),
]


def flatten(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=False, default=str)
    except Exception:
        return str(value)


def validate_filename(path: str) -> str | None:
    """Return an error message if the filename violates Pluto conventions."""
    if not path:
        return None
    basename = Path(path).name
    if basename in ("", ".", ".."):
        return None

    # Block spaces and other problematic characters
    if FILENAME_DENY_PATTERNS[0].search(basename):
        return (
            f"Pluto filename rule: '{basename}' contains spaces. "
            "Use '-' or '_' to separate words, e.g. 'my_file.md' or 'my-file.md'."
        )
    denied_char_match = FILENAME_DENY_PATTERNS[1].search(basename)
    if denied_char_match:
        return (
            f"Pluto filename rule: '{basename}' contains disallowed character "
            f"'{denied_char_match.group()}'. Use only letters, digits, '-', '_' and '.'."
        )

    # Block leading/trailing hyphens or dots on the basename stem
    stem = basename.rsplit(".", 1)[0] if "." in basename else basename
    if stem.startswith("-") or stem.startswith("."):
        return f"Pluto filename rule: '{basename}' must not start with '-' or '.'"
    if stem.endswith("-"):
        return f"Pluto filename rule: '{basename}' must not end with '-'"

    return None


def block(reason: str) -> int:
    print(json.dumps({"action": "block", "message": reason}, ensure_ascii=False))
    return 2


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except Exception as e:
        return block(f"Pluto pre-tool guard failed to parse hook payload: {e}")

    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input") or payload.get("args") or {}
    text = flatten(tool_input)
    is_pluto = any(marker in text for marker in ANDROMALIUS_MARKERS)
    has_approval = any(marker in text for marker in APPROVAL_MARKERS)
    filename_approved = FILENAME_APPROVAL_MARKER in text

    # Protect the migration scripts themselves from unversioned edits.
    touches_migration_script = any(
        name in text for name in [
            "update_pluto_manifests.py",
            "verify_pluto_manifests.py",
            "verify_hermes_skills.py",
        ]
    )
    is_write_tool = tool_name in {"write_file", "patch"}
    if is_write_tool and touches_migration_script and "bak-" not in text and not has_approval:
        return block("Pluto guard: migration/script verifier edits require a versioned backup before modification.")

    # Enforce filename conventions for write_file / patch
    if is_write_tool and not filename_approved:
        if tool_name == "write_file":
            path = str(tool_input.get("path") or "") if isinstance(tool_input, dict) else ""
            err = validate_filename(path)
            if err:
                return block(err)
        elif tool_name == "patch" and tool_input.get("mode", "replace") == "replace":
            path = str(tool_input.get("path") or "") if isinstance(tool_input, dict) else ""
            err = validate_filename(path)
            if err:
                return block(err)
        elif tool_name == "patch" and tool_input.get("mode") == "patch":
            # Inspect V4A patch headers for any disallowed filenames
            patch_text = str(tool_input.get("patch") or "")
            for line in patch_text.splitlines():
                m = re.match(r"\*{3}\s*(?:Update|Add)\s+File:\s*(.+)$", line)
                if m:
                    err = validate_filename(m.group(1).strip())
                    if err:
                        return block(err)

    if is_pluto and not has_approval:
        if tool_name == "terminal":
            command = str(tool_input.get("command") or "") if isinstance(tool_input, dict) else text
            if any(p.search(command) for p in DESTRUCTIVE_PATTERNS):
                return block("Pluto guard: destructive command touching ANDROMALIUS requires explicit approval and hash plan.")
        if tool_name in {"patch", "write_file"} and any(x in text for x in ["manifest_hashes.md", "main_manifest.md", "manifest_of_manifests.md"]):
            return block("Pluto guard: generated manifests must be changed by update_pluto_manifests.py, not hand-edited.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
