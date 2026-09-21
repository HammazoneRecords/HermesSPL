"""Notification checker — handles both config formats for thresholds."""

from typing import List, Union


class NotificationChecker:
    """Checks context ratio against thresholds and emits notifications."""

    def __init__(self, thresholds: Union[List[float], List[dict]] = None):
        self.thresholds = self._parse_thresholds(thresholds or [0.5, 0.6])
        self._notified = set()

    def _parse_thresholds(self, thresholds) -> List[float]:
        """Parse thresholds from either format:
        - Legacy: [0.5, 0.6]
        - Current config: [{"ratio": 0.5, "message": "..."}, ...]
        """
        result = []
        for t in thresholds:
            if isinstance(t, (int, float)):
                result.append(float(t))
            elif isinstance(t, dict):
                ratio = t.get("ratio")
                if ratio is not None:
                    result.append(float(ratio))
        return result

    def check(self, ratio: float, prompt_tokens: int, context_length: int) -> List[str]:
        """Check if any threshold is crossed. Returns list of notification messages."""
        notifications = []
        for threshold in self.thresholds:
            if ratio >= threshold and threshold not in self._notified:
                self._notified.add(threshold)
                pct = int(threshold * 100)
                notifications.append(
                    f"Context: {int(ratio * 100)}% full ({prompt_tokens:,}/{context_length:,} tokens) — "
                    f"Lane A threshold {pct}% reached"
                )
        return notifications

    def reset(self):
        """Reset notified thresholds (for new session)."""
        self._notified.clear()
