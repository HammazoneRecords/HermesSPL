#!/usr/bin/env python3
"""User preference capture and management module."""

import json
import os
from pathlib import Path
from typing import Any, Optional
import yaml


class Preferences:
    """Capture, store, and update user preferences locally."""

    def __init__(self, config_path: Optional[Path] = None):
        if config_path and not isinstance(config_path, Path):
            config_path = Path(config_path)
        self.config_path = config_path or Path(
            os.environ.get("HOME", "/root")
        ) / ".hermes" / "config.yaml"
        self.prefs_path = self.config_path.parent / "preferences.yaml"
        self._preferences: dict[str, Any] = self._load()

    def _load(self) -> dict[str, Any]:
        """Load preferences from local YAML file."""
        if self.prefs_path.exists():
            with open(self.prefs_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        return {}

    def save(self) -> None:
        """Persist preferences to local YAML file (privacy-first)."""
        self.prefs_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.prefs_path, "w", encoding="utf-8") as f:
            yaml.dump(self._preferences, f, default_flow_style=False, sort_keys=False)

    def set(self, section: str, key: str, value: Any) -> None:
        """Set a preference value under a section."""
        if section not in self._preferences:
            self._preferences[section] = {}
        self._preferences[section][key] = value
        self.save()

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get a preference value."""
        return self._preferences.get(section, {}).get(key, default)

    def capture_name(self, name: str) -> None:
        """Store user's preferred name."""
        self.set("identity", "name", name)

    def capture_pronouns(self, pronouns: str) -> None:
        """Store user's preferred pronouns."""
        self.set("identity", "pronouns", pronouns)

    def capture_schedule(self, work_start: str, work_end: str, timezone: str) -> None:
        """Store user's work schedule."""
        self.set("schedule", "work_start", work_start)
        self.set("schedule", "work_end", work_end)
        self.set("schedule", "timezone", timezone)

    def capture_comm_style(self, style: str) -> None:
        """Store preferred communication style."""
        self.set("communication", "style", style)

    def add_interest(self, interest: str) -> None:
        """Add an interest to the user's profile."""
        interests = self._preferences.get("interests", [])
        if interest not in interests:
            interests.append(interest)
        self._preferences["interests"] = interests
        self.save()

    def remove_interest(self, interest: str) -> None:
        """Remove an interest from the user's profile."""
        interests = self._preferences.get("interests", [])
        if interest in interests:
            interests.remove(interest)
            self._preferences["interests"] = interests
            self.save()

    def log_feedback(self, action: str, accepted: bool) -> None:
        """Log a feedback action (accepted/rejected suggestion)."""
        if "feedback" not in self._preferences:
            self._preferences["feedback"] = {"accepted": [], "rejected": []}
        bucket = "accepted" if accepted else "rejected"
        self._preferences["feedback"][bucket].append(action)
        self.save()

    def get_feedback_ratio(self) -> float:
        """Return accepted / total feedback ratio."""
        fb = self._preferences.get("feedback", {})
        accepted = len(fb.get("accepted", []))
        rejected = len(fb.get("rejected", []))
        total = accepted + rejected
        return accepted / total if total else 0.5

    def update_config_yaml(self) -> None:
        """Auto-update config.yaml based on observed behavior."""
        if not self.config_path.exists():
            return
        with open(self.config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

        # Adjust based on feedback ratio
        ratio = self.get_feedback_ratio()
        if "agent" not in config:
            config["agent"] = {}
        config["agent"]["feedback_acceptance_ratio"] = round(ratio, 3)

        # Store inferred work schedule
        schedule = self._preferences.get("schedule")
        if schedule:
            config["agent"]["user_timezone"] = schedule.get("timezone", "UTC")

        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    def snapshot(self) -> dict[str, Any]:
        """Return the full preference snapshot."""
        return dict(self._preferences)


def main() -> None:
    """Demo usage."""
    prefs = Preferences()
    prefs.capture_name("Alice")
    prefs.capture_pronouns("she/her")
    prefs.capture_schedule("09:00", "17:00", "America/New_York")
    prefs.capture_comm_style("concise")
    prefs.add_interest("machine learning")
    prefs.log_feedback("refactor suggestion", True)
    prefs.log_feedback("add type hints", False)
    print(json.dumps(prefs.snapshot(), indent=2))
    print(f"Feedback ratio: {prefs.get_feedback_ratio():.2f}")


if __name__ == "__main__":
    main()
