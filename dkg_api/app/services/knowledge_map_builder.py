from __future__ import annotations

from collections import defaultdict
from typing import Any


class KnowledgeMapBuilder:
    def build_clusters(
        self,
        concept_id: str,
        nodes: list[dict[str, Any]],
    ) -> list[dict[str, object]]:
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for node in nodes:
            grouped[
                self._cluster_name(
                    str(node.get("label") or node.get("id") or concept_id)
                )
            ].append(node)

        return [
            {
                "id": cluster_name,
                "label": cluster_name.replace("_", " ").title(),
                "core_nodes": [
                    node["id"]
                    for node in cluster_nodes
                    if node.get("epistemic_type") in {"core_fact", "doctrinal_view"}
                ],
                "peripheral_interpretations": [
                    node["id"]
                    for node in cluster_nodes
                    if node.get("epistemic_type")
                    in {"interpretive_view", "esoteric_view", "unknown"}
                ],
                "tradition_overlays": sorted(
                    {
                        str(node.get("tradition") or "shared_core")
                        for node in cluster_nodes
                    }
                ),
            }
            for cluster_name, cluster_nodes in sorted(grouped.items())
        ]

    def _cluster_name(self, label: str) -> str:
        lowered = label.lower()
        if any(token in lowered for token in ["death", "bardo"]):
            return "death_cluster"
        if any(token in lowered for token in ["nirvana", "liberation", "cessation"]):
            return "liberation_cluster"
        if any(token in lowered for token in ["emptiness", "sunyata"]):
            return "emptiness_cluster"
        if "karma" in lowered:
            return "karma_cluster"
        return "general_doctrine_cluster"
