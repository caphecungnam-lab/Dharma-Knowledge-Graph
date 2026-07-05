from __future__ import annotations

from collections import Counter
from typing import Any


class EpistemicMonitor:
    def snapshot(
        self,
        *,
        accepted_nodes: list[dict[str, Any]] | None = None,
        rejections: list[dict[str, Any]] | None = None,
    ) -> dict[str, object]:
        nodes = accepted_nodes or []
        rejected = rejections or []
        total = len(nodes) + len(rejected)
        types = Counter(self._epistemic_type(node) for node in nodes)
        conflicts = sum(
            1
            for node in nodes
            if (node.get("conflict") or {}).get("type") not in {None, "", "none"}
        )

        return {
            "core_fact_ratio": self._ratio(types["core_fact"], len(nodes)),
            "doctrinal_ratio": self._ratio(
                types["doctrinal"] + types["doctrinal_view"],
                len(nodes),
            ),
            "interpretive_ratio": self._ratio(
                types["interpretive"] + types["interpretive_view"],
                len(nodes),
            ),
            "esoteric_ratio": self._ratio(
                types["esoteric"] + types["esoteric_view"],
                len(nodes),
            ),
            "acceptance_rate": self._ratio(len(nodes), total),
            "rejection_rate": self._ratio(len(rejected), total),
            "conflict_rate": self._ratio(conflicts, len(nodes)),
            "truth_engine_rejection_rate": self._ratio(len(rejected), total),
            "epistemic_type_distribution": dict(types),
            "confidence_distribution": self._confidence_distribution(nodes),
        }

    def snapshot_from_report(self, report: dict[str, Any]) -> dict[str, object]:
        nodes = []
        rejections = []
        for document in report.get("documents", []):
            nodes.extend(document.get("accepted_nodes", []))
            rejections.extend(document.get("rejections", []))
        return self.snapshot(accepted_nodes=nodes, rejections=rejections)

    def _epistemic_type(self, node: dict[str, Any]) -> str:
        value = str(node.get("epistemic_type") or "unknown")
        if value == "doctrinal_view":
            return "doctrinal"
        if value == "interpretive_view":
            return "interpretive"
        if value == "esoteric_view":
            return "esoteric"
        return value

    def _confidence_distribution(self, nodes: list[dict[str, Any]]) -> dict[str, int]:
        buckets = Counter()
        for node in nodes:
            confidence = float(node.get("confidence") or 0.0)
            if confidence >= 0.9:
                buckets["high"] += 1
            elif confidence >= 0.7:
                buckets["medium_high"] += 1
            elif confidence >= 0.5:
                buckets["medium"] += 1
            else:
                buckets["low"] += 1
        return dict(buckets)

    def _ratio(self, numerator: int, denominator: int) -> float:
        if denominator <= 0:
            return 0.0
        return round(numerator / denominator, 3)
