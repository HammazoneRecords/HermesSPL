"""
Tests for threshold config parsing fix.
The current plugin expects list of floats but config.yaml stores list of objects.
"""

import pytest
from lane_a_context_engine.notifications import NotificationChecker


class TestThresholdConfigParsing:
    """Test that notification thresholds parse both config formats."""

    def test_parse_float_list_format(self):
        """Should handle legacy format: [0.5, 0.6]."""
        checker = NotificationChecker(thresholds=[0.5, 0.6])
        assert checker.thresholds == [0.5, 0.6]

    def test_parse_object_list_format(self):
        """Should handle current config format: [{"ratio": 0.5, "message": "..."}]."""
        checker = NotificationChecker(thresholds=[
            {"ratio": 0.5, "message": "Context at 50%"},
            {"ratio": 0.6, "message": "Context at 60%"},
        ])
        assert checker.thresholds == [0.5, 0.6]

    def test_parse_mixed_list_format(self):
        """Should handle mixed format gracefully."""
        checker = NotificationChecker(thresholds=[
            {"ratio": 0.5, "message": "50%"},
            0.6,
        ])
        assert checker.thresholds == [0.5, 0.6]

    def test_default_thresholds(self):
        """Should default to [0.5, 0.6] if no config provided."""
        checker = NotificationChecker()
        assert checker.thresholds == [0.5, 0.6]

    def test_check_emits_at_threshold(self):
        """Should emit notification when ratio crosses threshold."""
        checker = NotificationChecker(thresholds=[0.5])
        notifications = checker.check(0.51, 100000, 200000)
        assert len(notifications) >= 1
        assert any("50%" in n for n in notifications)

    def test_check_no_emit_below_threshold(self):
        """Should NOT emit notification when ratio is below threshold."""
        checker = NotificationChecker(thresholds=[0.5, 0.6])
        notifications = checker.check(0.4, 80000, 200000)
        assert len(notifications) == 0

    def test_check_no_duplicate_notifications(self):
        """Should NOT re-notify for same threshold twice."""
        checker = NotificationChecker(thresholds=[0.5])
        n1 = checker.check(0.51, 100000, 200000)
        n2 = checker.check(0.52, 104000, 200000)
        # First should emit, second should not (already notified)
        assert len(n1) >= 1
        assert len(n2) == 0
