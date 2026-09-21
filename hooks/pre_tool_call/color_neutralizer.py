#!/usr/bin/env python3
"""Color Neutralizer Hook — Pre-RITE Refinement Stage for HermesSPL.

Scrubs false contrasts from tool inputs before they enter the RITE cycle.
Detects extreme binary framing, loaded language, and emotional manipulation;
neutralizes them into balanced form. Logs original vs neutralized input.

Hook events: pre_tool_call
Matcher: * (all tools)

Input (stdin): JSON payload from Hermes
  {"tool_name": "...", "tool_input": {...}, ...}

Output (stdout): JSON
  {"action": "allow", "reason": "...", "neutralized_input": {...}}
  or {"action": "block", "reason": "..."}
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = Path("/root/MW_CENTRAL/EARTH-MOON/hermes-spl-fork")
SHIMMER_LOG = ROOT / ".hermes" / "rite_shimmer_log.jsonl"

# ---------------------------------------------------------------------------
# False Contrast Detection Patterns
# ---------------------------------------------------------------------------

# Binary framing: forces a choice between two extremes
BINARY_FRAMING_PATTERNS = [
    re.compile(r"\b(either\s+or|black\s+and\s+white|all\s+or\s+nothing)\b", re.I),
    re.compile(r"\b(always\s+vs\s+never|right\s+vs\s+wrong|good\s+vs\s+evil)\b", re.I),
    re.compile(r"\b(with\s+me\s+or\s+against\s+me|for\s+us\s+or\s+against\s+us)\b", re.I),
    re.compile(r"\b(perfection\s+or\s|success\s+or\s+failure|win\s+or\s+die)\b", re.I),
]

# Loaded language: emotionally charged words designed to provoke
LOADED_LANGUAGE_PATTERNS = [
    re.compile(r"\b(obviously\s+wrong|clearly\s+stupid|undeniably\s+false)\b", re.I),
    re.compile(r"\b(everyone\s+knows|nobody\s+with\s+a\s+brain)\b", re.I),
    re.compile(r"\b(catastrophic\s+failure|total\s+disaster|complete\s+destruction)\b", re.I),
    re.compile(r"\b(they\s+always|they\s+never|those\s+people)\b", re.I),
    re.compile(r"\b(unthinkable|inconceivable|impossible\s+to\s+imagine)\b", re.I),
]

# Emotional manipulation: urgency/fear-based pressure tactics
EMOTIONAL_MANIPULATION_PATTERNS = [
    re.compile(r"\b(act\s+now\s+or\s+never|last\s+chance|final\s+warning)\b", re.I),
    re.compile(r"\b(before\s+it['']?s\s+too\s+late|time\s+is\s+running\s+out)\b", re.I),
    re.compile(r"\b(if\s+you\s+don['']?t\b.*?\bdisaster|destroy|collapse)\b", re.I),
    re.compile(r"\b(must\s+(absolutely|certainly|definitely)\b.*?or\s+(else|otherwise))", re.I),
    re.compile(r"\b(urgent|emergency|critical|crisis)\b.*!\s*$", re.I),
]

# Irredeemable toxicity patterns (rare block condition)
TOXIC_PATTERNS = [
    re.compile(r"\b(kill\s+(yourself|himself|herself|themselves|myself))\b", re.I),
    re.compile(r"\b(kill\s+(all|every|the)\b.*?((people|person|man|woman|child|children)))\b", re.I),
    re.compile(r"\b(bomb\s+(the|that|this|my|your|our))\b", re.I),
    re.compile(r"\b(terrorist\s+attack|mass\s+shooting|suicide\s+bomb)\b", re.I),
    re.compile(r"\b(child\s+(porn|abuse|molestation))\b", re.I),
]

ALL_PATTERNS = {
    "binary_framing": BINARY_FRAMING_PATTERNS,
    "loaded_language": LOADED_LANGUAGE_PATTERNS,
    "emotional_manipulation": EMOTIONAL_MANIPULATION_PATTERNS,
}

# ---------------------------------------------------------------------------
# Neutralization Rules
# ---------------------------------------------------------------------------

NEUTRALIZATION_MAP = {
    # Binary → spectrum
    "either or": "consider multiple options",
    "black and white": "acknowledge nuance",
    "all or nothing": "consider partial approaches",
    "with me or against me": "recognize varied perspectives",
    "for us or against us": "acknowledge diverse viewpoints",
    "perfection or": "progress over perfection",
    "success or failure": "learning opportunity",
    "win or die": "strive for positive outcome",
    # Loaded → neutral
    "obviously wrong": "appears incorrect",
    "clearly stupid": "seems unwise",
    "undeniably false": "appears inaccurate",
    "everyone knows": "some believe",
    "nobody with a brain": "few would argue",
    "catastrophic failure": "significant setback",
    "total disaster": "serious problem",
    "complete destruction": "major damage",
    "they always": "they sometimes",
    "they never": "they rarely",
    "those people": "some groups",
    "unthinkable": "unlikely",
    "inconceivable": "improbable",
    "impossible to imagine": "difficult to envision",
    # Emotional manipulation → balanced
    "act now or never": "consider timely action",
    "last chance": "current opportunity",
    "final warning": "important notice",
    "before it's too late": "while time remains",
    "time is running out": "time is limited",
    "must absolutely": "should consider",
    "must certainly": "should evaluate",
    "must definitely": "should assess",
}


def flatten_input(tool_input: dict[str, Any] | None) -> str:
    """Flatten tool input to string for analysis."""
    if not tool_input:
        return ""
    try:
        return json.dumps(tool_input, ensure_ascii=False, default=str)
    except Exception:
        return str(tool_input)


def detect_false_contrasts(text: str) -> list[dict[str, str]]:
    """Detect false contrasts in text. Returns list of {type, pattern, match}."""
    detections = []
    for category, patterns in ALL_PATTERNS.items():
        for pat in patterns:
            match = pat.search(text)
            if match:
                detections.append({
                    "type": category,
                    "pattern": pat.pattern,
                    "match": match.group(),
                })
    return detections


def detect_toxicity(text: str) -> list[dict[str, str]]:
    """Detect irredeemable toxicity. Returns list of matches."""
    toxic = []
    for pat in TOXIC_PATTERNS:
        match = pat.search(text)
        if match:
            toxic.append({"pattern": pat.pattern, "match": match.group()})
    return toxic


def neutralize_text(text: str, detections: list[dict[str, str]]) -> str:
    """Apply neutralization to text based on detected false contrasts."""
    if not detections:
        return text

    neutralized = text
    for detection in detections:
        match_text = detection["match"].lower()
        # Check if we have a direct replacement
        replacement = None
        for key, val in NEUTRALIZATION_MAP.items():
            if key in match_text:
                replacement = val
                break

        if replacement:
            # Case-insensitive replacement of the matched text
            pattern = re.compile(re.escape(detection["match"]), re.I)
            neutralized = pattern.sub(replacement, neutralized, count=1)
        else:
            # Generic neutralization marker
            pattern = re.compile(re.escape(detection["match"]), re.I)
            neutralized = pattern.sub("[neutralized]", neutralized, count=1)

    return neutralized


def neutralize_input(tool_input: dict[str, Any], detections: list[dict[str, str]]) -> dict[str, Any]:
    """Neutralize false contrasts in tool input dict."""
    if not detections or not tool_input:
        return tool_input

    # Deep copy and neutralize string values recursively
    def _neutralize_value(value: Any) -> Any:
        if isinstance(value, str):
            return neutralize_text(value, detections)
        if isinstance(value, dict):
            return {k: _neutralize_value(v) for k, v in value.items()}
        if isinstance(value, list):
            return [_neutralize_value(item) for item in value]
        return value

    return _neutralize_value(tool_input)


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def log_neutralization(
    tool_name: str,
    original_text: str,
    neutralized_text: str,
    detections: list[dict[str, str]],
    action: str,
    reason: str,
) -> None:
    """Log neutralization event to shimmer log."""
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "hook": "color_neutralizer",
        "tool_name": tool_name,
        "action": action,
        "reason": reason,
        "detections": detections,
        "original_excerpt": original_text[:500],
        "neutralized_excerpt": neutralized_text[:500],
        "neutralization_count": len(detections),
    }
    SHIMMER_LOG.parent.mkdir(parents=True, exist_ok=True)
    with SHIMMER_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")


# ---------------------------------------------------------------------------
# Main Enforcement Function
# ---------------------------------------------------------------------------

def enforce(tool_name: str, tool_input: dict[str, Any]) -> dict[str, Any]:
    """Enforce color neutralization on tool input.

    Returns:
        {"action": "allow", "reason": "...", "neutralized_input": {...}}
        or {"action": "block", "reason": "..."}
    """
    text = flatten_input(tool_input)

    # Check for irredeemable toxicity first (rare block condition)
    toxic = detect_toxicity(text)
    if toxic:
        matches = "; ".join(t["match"] for t in toxic)
        reason = f"IRREDEEMABLE TOXICITY: Blocked due to harmful content ({matches})"
        log_neutralization(tool_name, text, text, toxic, "block", reason)
        return {"action": "block", "reason": reason}

    # Detect false contrasts
    detections = detect_false_contrasts(text)

    # No false contrasts detected — pass through unchanged
    if not detections:
        return {
            "action": "allow",
            "reason": "clean — no false contrasts detected",
            "neutralized_input": tool_input,
        }

    # Apply neutralization
    neutralized_text = neutralize_text(text, detections)
    neutralized_input = neutralize_input(tool_input, detections)

    # Build reason summary
    categories = sorted(set(d["type"] for d in detections))
    reason = (
        f"NEUTRALIZED: {len(detections)} false contrast(s) detected "
        f"({', '.join(categories)}) — reframed into balanced form"
    )

    log_neutralization(tool_name, text, neutralized_text, detections, "allow", reason)

    return {
        "action": "allow",
        "reason": reason,
        "neutralized_input": neutralized_input,
    }


# ---------------------------------------------------------------------------
# Entry Point (for hook execution via stdin/stdout)
# ---------------------------------------------------------------------------

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

    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input") or payload.get("args") or {}

    if not tool_name:
        return 0

    try:
        result = enforce(tool_name, tool_input)
    except Exception as e:
        # Color Neutralizer must never crash the hook chain
        return 0

    if result["action"] == "block":
        print(json.dumps(result, ensure_ascii=False))
        return 2

    # For allow, output the neutralized result
    print(json.dumps(result, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
