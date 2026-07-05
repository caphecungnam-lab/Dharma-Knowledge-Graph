from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class TimelineTracker:
    def build(self, reports: list[dict[str, Any]]) -> dict[str, object]:
        series = []
        for report in reports:
            timestamp = str(report.get("timestamp") or self._now())
            nodes = int(report.get("nodes_accepted") or 0)
            rejected = int(report.get("nodes_rejected") or 0)
            conflicts = len(report.get("conflict_clusters_detected") or [])
            total = nodes + rejected
            series.append(
                {
                    "timestamp": timestamp,
                    "drift_score": self._drift_score(report),
                    "node_growth": nodes,
                    "conflict_rate": round(conflicts / nodes, 3) if nodes else 0.0,
                    "rejection_rate": round(rejected / total, 3) if total else 0.0,
                }
            )
        return {"time_series": series}

    def build_from_paths(self, paths: list[Path]) -> dict[str, object]:
        import json

        reports = []
        for path in paths:
            if not path.exists():
                continue
            report = json.loads(path.read_text(encoding="utf-8"))
            report["timestamp"] = datetime.fromtimestamp(
                path.stat().st_mtime,
                tz=timezone.utc,
            ).isoformat()
            reports.append(report)
        return self.build(reports)

    def _drift_score(self, report: dict[str, Any]) -> float:
        drift = report.get("drift_signals_detected") or {}
        if not drift.get("drift_detected"):
            return 0.0
        severity = drift.get("severity")
        if severity == "high":
            return 1.0
        if severity == "medium":
            return 0.6
        return 0.3

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()
