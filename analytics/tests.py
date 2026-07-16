from django.test import TestCase

from .services import get_dashboard_metrics


class AnalyticsServiceTests(TestCase):
    def test_dashboard_metrics_returns_expected_keys(self):
        class DummyUser:
            id = 1
            is_authenticated = True

        metrics = get_dashboard_metrics(DummyUser())

        self.assertIn("total_applications", metrics)
        self.assertIn("shortlisted", metrics)
        self.assertIn("rejected", metrics)
        self.assertIn("pending", metrics)
        self.assertIn("status_breakdown", metrics)
