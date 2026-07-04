from __future__ import annotations

from collections import defaultdict
from typing import Any


class ContradictionMiner:
    def mine(self, nodes: list[dict[str, Any]]) -> list[dict[str, object]]:
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for node in nodes:
            grouped[str(node.get("label") or "")].append(node)

        contradictions = []
        for concept, concept_nodes in grouped.items():
            traditions = {
                str(node.get("tradition") or "")
                for node in concept_nodes
                if node.get("tradition")
            }
            if len(traditions) < 2:
                continue

            conflict_type = self._conflict_type(concept, concept_nodes)
            tradition_list = sorted(traditions)
            contradictions.append(
                {
                    "concept": concept,
                    "conflict_type": conflict_type,
                    "tradition_a": tradition_list[0],
                    "tradition_b": tradition_list[-1],
                    "severity": self._severity(conflict_type),
                }
            )

        return contradictions

    def _conflict_type(self, concept: str, nodes: list[dict[str, Any]]) -> str:
        text = " ".join(str(node.get("text") or "") for node in nodes).lower()
        if concept == "death" and "bardo" in text:
            return "doctrinal"
        if any(marker in text for marker in ["ultimate reality", "ontology"]):
            return "ontological"
        if any(marker in text for marker in ["same meaning", "different wording"]):
            return "semantic"
        return "doctrinal"

    def _severity(self, conflict_type: str) -> float:
        return {
            "semantic": 0.25,
            "doctrinal": 0.7,
            "ontological": 0.9,
        }.get(conflict_type, 0.0)
