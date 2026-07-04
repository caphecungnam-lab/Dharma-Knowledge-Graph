from __future__ import annotations

from typing import Any

from dkg_api.app.services.epistemic_ui_adapter import TRADITIONS


class TraditionOverlayEngine:
    def build_overlay(
        self,
        concept_id: str,
        nodes: list[dict[str, Any]],
        edges: list[dict[str, Any]],
    ) -> dict[str, object]:
        overlays = {}
        for tradition in TRADITIONS:
            overlays[tradition] = {
                "concept_id": concept_id,
                "nodes": [
                    node for node in nodes if self._belongs_to_layer(node, tradition)
                ],
                "edges": [
                    edge
                    for edge in edges
                    if edge.get("from") in self._node_ids(nodes, tradition)
                    or edge.get("to") in self._node_ids(nodes, tradition)
                ],
                "semantic_emphasis": self._emphasis(tradition),
            }
        return overlays

    def _belongs_to_layer(self, node: dict[str, Any], tradition: str) -> bool:
        node_tradition = str(node.get("tradition") or "").lower()
        return node_tradition in {tradition, "shared_core"}

    def _node_ids(self, nodes: list[dict[str, Any]], tradition: str) -> set[str]:
        return {
            str(node.get("id"))
            for node in nodes
            if self._belongs_to_layer(node, tradition)
        }

    def _emphasis(self, tradition: str) -> list[str]:
        return {
            "theravada": ["impermanence", "cessation"],
            "mahayana": ["emptiness", "non-duality"],
            "vajrayana": ["bardo", "transformation"],
        }[tradition]
