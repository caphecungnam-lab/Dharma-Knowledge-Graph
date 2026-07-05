from __future__ import annotations

import unittest

from dkg_api.app.observability.alerts import AlertEngine
from dkg_api.app.observability.conflict_map import ConflictMap
from dkg_api.app.observability.dashboard import SystemHealthDashboard
from dkg_api.app.observability.drift_detector import DriftDetector
from dkg_api.app.observability.epistemic_monitor import EpistemicMonitor
from dkg_api.app.observability.timeline_tracker import TimelineTracker
from scripts.day5_drift_simulation import run_simulation


class Day5ObservabilityTest(unittest.TestCase):
    def sample_nodes(self):
        return [
            {
                "node_id": "concept_death",
                "tradition": "theravada",
                "epistemic_type": "doctrinal_view",
                "confidence": 0.8,
                "conflict": {"type": "none", "severity": 0.0},
                "match": {"definition": "Death is described one way."},
            },
            {
                "node_id": "concept_death",
                "tradition": "vajrayana",
                "epistemic_type": "esoteric_view",
                "confidence": 0.7,
                "conflict": {"type": "doctrinal", "severity": 0.7},
                "match": {"definition": "Death is described another way."},
            },
        ]

    def test_epistemic_monitor_snapshot_reports_rates(self):
        snapshot = EpistemicMonitor().snapshot(
            accepted_nodes=self.sample_nodes(),
            rejections=[{"reason": "low_confidence"}],
        )

        self.assertEqual(snapshot["rejection_rate"], 0.333)
        self.assertGreater(snapshot["doctrinal_ratio"], 0)
        self.assertGreater(snapshot["esoteric_ratio"], 0)

    def test_drift_detector_flags_epistemic_drift(self):
        drift = DriftDetector().detect(self.sample_nodes())

        self.assertTrue(drift["drift_detected"])
        self.assertEqual(drift["severity"], "high")
        self.assertEqual(drift["drift_type"], "epistemic")

    def test_conflict_map_does_not_merge_conflicts(self):
        conflict_map = ConflictMap().build(self.sample_nodes())

        self.assertEqual(conflict_map["conflict_count"], 1)
        self.assertEqual(conflict_map["edges"][0]["label"], "DOCTRINAL_VARIATION")

    def test_timeline_tracker_outputs_series(self):
        timeline = TimelineTracker().build(
            [
                {
                    "timestamp": "2026-07-05T00:00:00Z",
                    "nodes_accepted": 10,
                    "nodes_rejected": 2,
                    "conflict_clusters_detected": [{}],
                    "drift_signals_detected": {"drift_detected": True, "severity": "medium"},
                }
            ]
        )

        self.assertEqual(len(timeline["time_series"]), 1)
        self.assertEqual(timeline["time_series"][0]["drift_score"], 0.6)

    def test_alerts_trigger_on_high_drift(self):
        alerts = AlertEngine().evaluate(
            monitor_snapshot={"rejection_rate": 0.1, "conflict_rate": 0.0},
            drift={"drift_detected": True, "severity": "high"},
        )

        self.assertIn("CRITICAL", {alert["level"] for alert in alerts})

    def test_dashboard_returns_structured_health(self):
        dashboard = SystemHealthDashboard().build()

        self.assertIn(dashboard["system_state"], {"stable", "warning", "unstable"})
        self.assertIn("graph_health", dashboard)
        self.assertIn("epistemic_health", dashboard)

    def test_drift_simulation_detects_and_keeps_conflicts_visible(self):
        report = run_simulation()

        self.assertTrue(report["drift"]["drift_detected"])
        self.assertEqual(report["merge_policy"], "conflicts_visible_not_merged")
        self.assertGreaterEqual(report["conflict_map"]["conflict_count"], 1)


if __name__ == "__main__":
    unittest.main()
