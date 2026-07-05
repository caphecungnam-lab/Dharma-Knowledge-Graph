from __future__ import annotations

from collections import defaultdict
from typing import Any


class DriftDetector:
    def detect(self, nodes: list[dict[str, Any]]) -> dict[str, object]:
        concepts: dict[str, dict[str, set[str]]] = defaultdict(
            lambda: {
                "definitions": set(),
                "epistemic_types": set(),
                "traditions": set(),
            }
        )
        confidence_values: dict[str, list[float]] = defaultdict(list)

        for node in nodes:
            concept = str(node.get("node_id") or node.get("id") or "")
            if not concept:
                continue
            match = node.get("match") or {}
            concepts[concept]["definitions"].add(
                self._normalize_text(match.get("definition") or match.get("text") or "")
            )
            concepts[concept]["epistemic_types"].add(
                str(node.get("epistemic_type") or "unknown")
            )
            concepts[concept]["traditions"].add(str(node.get("tradition") or "unknown"))
            confidence_values[concept].append(float(node.get("confidence") or 0.0))

        affected: list[str] = []
        drift_types = set()
        for concept, values in concepts.items():
            if len({item for item in values["definitions"] if item}) > 1:
                affected.append(concept)
                drift_types.add("semantic")
            if len(values["epistemic_types"]) > 1:
                affected.append(concept)
                drift_types.add("epistemic")
            if len(values["traditions"]) > 1:
                affected.append(concept)
                drift_types.add("structural")
            if self._confidence_instability(confidence_values[concept]):
                affected.append(concept)
                drift_types.add("epistemic")

        unique_affected = sorted(set(affected))
        return {
            "drift_detected": bool(unique_affected),
            "severity": self._severity(unique_affected, drift_types),
            "affected_concepts": unique_affected,
            "drift_type": self._drift_type(drift_types),
        }

    def detect_from_report(self, report: dict[str, Any]) -> dict[str, object]:
        nodes = []
        for document in report.get("documents", []):
            nodes.extend(document.get("accepted_nodes", []))
        return self.detect(nodes)

    def _confidence_instability(self, values: list[float]) -> bool:
        if len(values) < 2:
            return False
        return max(values) - min(values) > 0.25

    def _severity(self, affected: list[str], drift_types: set[str]) -> str:
        if "epistemic" in drift_types or len(affected) >= 5:
            return "high"
        if affected:
            return "medium"
        return "low"

    def _drift_type(self, drift_types: set[str]) -> str:
        if "epistemic" in drift_types:
            return "epistemic"
        if "semantic" in drift_types:
            return "semantic"
        if "structural" in drift_types:
            return "structural"
        return "none"

    def _normalize_text(self, value: object) -> str:
        return " ".join(str(value or "").lower().split())
