from __future__ import annotations

from collections import Counter
from typing import Any

from dkg_api.app.services.conflict_analyzer import ConflictAnalyzer
from dkg_api.app.services.epistemic_classifier import classify_epistemic_type
from dkg_api.app.services.traceability_engine import TraceabilityEngine


class EpistemicTruthSystem:
    def __init__(self) -> None:
        self.conflict_analyzer = ConflictAnalyzer()
        self.traceability_engine = TraceabilityEngine()

    def evaluate(self, nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
        enriched_nodes = []
        traditions = self._tradition_counts(nodes)
        for node in nodes:
            epistemic_type = classify_epistemic_type(node)
            conflict = self.conflict_analyzer.analyze(node)
            tradition_alignment = self.map_tradition_alignment(node)
            traceability = self.traceability_engine.attach(node)
            confidence = self.compute_confidence(
                node,
                epistemic_type,
                conflict,
                traditions,
                traceability,
            )
            ai_usage_allowed = self.ai_usage_allowed(
                epistemic_type,
                confidence,
                traceability,
            )
            match = node.get("match", {})

            enriched_nodes.append(
                {
                    "node_id": str(match.get("node_id") or ""),
                    "epistemic_type": epistemic_type,
                    "confidence": confidence,
                    "tradition_alignment": tradition_alignment,
                    "conflict": conflict,
                    "traceability": traceability,
                    "ai_usage_allowed": ai_usage_allowed,
                    "match": match,
                    "related": node.get("related", []),
                    "tradition": str(match.get("tradition") or "unknown"),
                }
            )

        return enriched_nodes

    def filter_ai_usable(
        self,
        evaluated_nodes: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        return [
            node for node in evaluated_nodes if node.get("ai_usage_allowed") is True
        ]

    def compute_confidence(
        self,
        node: dict[str, Any],
        epistemic_type: str,
        conflict: dict[str, object],
        traditions: Counter[str],
        traceability: dict[str, object],
    ) -> float:
        match = node.get("match", {})
        confidence = max(0.0, min(float(match.get("score") or 0.0), 1.0))

        if epistemic_type == "unknown":
            confidence = min(confidence, 0.4)
        elif epistemic_type == "core_fact":
            confidence = max(confidence, 0.75)
        elif epistemic_type == "doctrinal_view":
            confidence = max(confidence, 0.65)
        elif epistemic_type == "interpretive_view":
            confidence = min(max(confidence, 0.5), 0.75)
        elif epistemic_type == "esoteric_view":
            confidence = min(max(confidence, 0.5), 0.7)

        if len(traditions) > 1:
            confidence += 0.1

        confidence -= float(conflict.get("severity") or 0.0) * 0.35

        if not self.traceability_engine.has_trace(traceability):
            confidence = min(confidence, 0.4)

        return round(max(0.0, min(confidence, 1.0)), 3)

    def map_tradition_alignment(self, node: dict[str, Any]) -> dict[str, str]:
        traditions = self._node_traditions(node)
        alignment = {
            "theravada": "none",
            "mahayana": "none",
            "vajrayana": "none",
        }
        for tradition in alignment:
            if tradition in traditions:
                alignment[tradition] = "aligned"
        if len(traditions) > 1:
            for tradition, value in alignment.items():
                if value == "none":
                    alignment[tradition] = "partial"
        return alignment

    def ai_usage_allowed(
        self,
        epistemic_type: str,
        confidence: float,
        traceability: dict[str, object],
    ) -> bool:
        return (
            epistemic_type != "unknown"
            and confidence >= 0.5
            and self.traceability_engine.has_trace(traceability)
        )

    def _tradition_counts(self, nodes: list[dict[str, Any]]) -> Counter[str]:
        traditions = []
        for node in nodes:
            traditions.extend(self._node_traditions(node))
        return Counter(traditions)

    def _node_traditions(self, node: dict[str, Any]) -> set[str]:
        match = node.get("match", {})
        traditions = {str(match.get("tradition") or "").lower().strip()}
        for related in node.get("related", []):
            traditions.add(str(related.get("tradition") or "").lower().strip())
        return {tradition for tradition in traditions if tradition}
