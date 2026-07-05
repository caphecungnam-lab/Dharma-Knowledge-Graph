from __future__ import annotations

from typing import Any


class AlertEngine:
    def evaluate(
        self,
        *,
        monitor_snapshot: dict[str, Any],
        drift: dict[str, Any],
        dashboard: dict[str, Any] | None = None,
    ) -> list[dict[str, object]]:
        alerts = []
        rejection_rate = float(monitor_snapshot.get("rejection_rate") or 0.0)
        conflict_rate = float(monitor_snapshot.get("conflict_rate") or 0.0)

        if drift.get("severity") == "high":
            alerts.append(self._alert("CRITICAL", "epistemic_drift_high"))
        elif drift.get("drift_detected"):
            alerts.append(self._alert("WARNING", "epistemic_drift_detected"))

        if rejection_rate > 0.5:
            alerts.append(self._alert("CRITICAL", "rejection_rate_spike"))
        elif rejection_rate > 0.2:
            alerts.append(self._alert("WARNING", "rejection_rate_elevated"))

        if conflict_rate > 0.25:
            alerts.append(self._alert("WARNING", "conflict_density_increased"))

        if dashboard and dashboard.get("system_state") == "unstable":
            alerts.append(self._alert("CRITICAL", "ingestion_unstable"))

        if not alerts:
            alerts.append(self._alert("INFO", "observability_nominal"))
        return alerts

    def _alert(self, level: str, reason: str) -> dict[str, object]:
        return {
            "level": level,
            "reason": reason,
        }
