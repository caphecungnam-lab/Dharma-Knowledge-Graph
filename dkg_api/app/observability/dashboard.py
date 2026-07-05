from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from dkg_api.app.observability.alerts import AlertEngine
from dkg_api.app.observability.conflict_map import ConflictMap
from dkg_api.app.observability.drift_detector import DriftDetector
from dkg_api.app.observability.epistemic_monitor import EpistemicMonitor
from dkg_api.app.observability.metrics import metrics


DAY4_REPORT = Path("reports/day4_corpus_report.json")
GRAPH_JSON = Path("data/processed/graph.json")


class SystemHealthDashboard:
    def build(self, report_path: Path = DAY4_REPORT) -> dict[str, object]:
        report = self._load_json(report_path, default={})
        graph = self._load_json(GRAPH_JSON, default={})
        monitor = EpistemicMonitor().snapshot_from_report(report)
        drift = DriftDetector().detect_from_report(report)
        conflict_map = ConflictMap().build_from_report(report)
        runtime = metrics.health_metrics()

        dashboard = {
            "system_state": self._system_state(monitor, drift),
            "graph_health": self._graph_health(graph),
            "ingestion_health": {
                "throughput": int(report.get("nodes_accepted") or 0),
                "rejection_rate": monitor["rejection_rate"],
            },
            "safety_health": {
                "injection_attempts_blocked": 0,
                "bypass_attempts": 0,
                "truth_rejection_rate": runtime["truth_rejection_rate"],
            },
            "epistemic_health": {
                "drift_score": self._drift_score(drift),
                "conflict_density": monitor["conflict_rate"],
            },
        }
        dashboard["alerts"] = AlertEngine().evaluate(
            monitor_snapshot=monitor,
            drift=drift,
            dashboard=dashboard,
        )
        dashboard["conflict_map_summary"] = {
            "nodes": len(conflict_map["nodes"]),
            "edges": len(conflict_map["edges"]),
        }
        return dashboard

    def _graph_health(self, graph: dict[str, Any]) -> dict[str, int]:
        nodes = graph.get("nodes") or []
        relationships = graph.get("relationships") or []
        linked = set()
        for relationship in relationships:
            linked.add(str(relationship.get("source") or relationship.get("from") or ""))
            linked.add(str(relationship.get("target") or relationship.get("to") or ""))
        orphan_nodes = [
            node for node in nodes if str(node.get("id") or "") not in linked
        ]
        invalid_nodes = [
            node for node in nodes if not node.get("id") or not node.get("type")
        ]
        return {
            "total_nodes": len(nodes),
            "orphan_nodes": len(orphan_nodes),
            "invalid_nodes": len(invalid_nodes),
        }

    def _system_state(
        self,
        monitor: dict[str, Any],
        drift: dict[str, Any],
    ) -> str:
        if drift.get("severity") == "high" or float(monitor["rejection_rate"]) > 0.5:
            return "unstable"
        if drift.get("drift_detected") or float(monitor["rejection_rate"]) > 0.2:
            return "warning"
        return "stable"

    def _drift_score(self, drift: dict[str, Any]) -> float:
        if drift.get("severity") == "high":
            return 1.0
        if drift.get("severity") == "medium":
            return 0.6
        if drift.get("drift_detected"):
            return 0.3
        return 0.0

    def _load_json(self, path: Path, *, default: dict[str, Any]) -> dict[str, Any]:
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))
