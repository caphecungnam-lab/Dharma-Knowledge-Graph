from __future__ import annotations

import math
from typing import Any

TRADITIONS = ("theravada", "mahayana", "vajrayana")


class EpistemicUIAdapter:
    def node(
        self,
        raw_node: dict[str, Any],
        index: int,
        total: int,
    ) -> dict[str, object]:
        confidence = float(
            raw_node.get("confidence") or raw_node.get("last_confidence") or 0.5
        )
        angle = (2 * math.pi * index) / max(total, 1)
        radius = 1.0 if index == 0 else 4.0
        return {
            "id": str(raw_node.get("id") or raw_node.get("node_id") or ""),
            "label": str(raw_node.get("label") or raw_node.get("id") or ""),
            "position": {
                "x": round(math.cos(angle) * radius, 3),
                "y": round(math.sin(angle) * radius, 3),
                "z": round(1.0 - confidence, 3),
            },
            "epistemic_type": str(raw_node.get("epistemic_type") or "unknown"),
            "confidence": confidence,
            "visual_state": self.visual_state(confidence),
            "tradition": str(raw_node.get("tradition") or "shared_core"),
        }

    def edge(self, raw_edge: dict[str, Any]) -> dict[str, object]:
        strength = float(raw_edge.get("strength") or raw_edge.get("confidence") or 0.7)
        edge_type = str(raw_edge.get("type") or "RELATED_TO")
        return {
            "from": str(raw_edge.get("from") or raw_edge.get("source") or ""),
            "to": str(raw_edge.get("to") or raw_edge.get("target") or ""),
            "type": edge_type,
            "strength": max(0.0, min(strength, 1.0)),
            "visual_label": self.edge_label(edge_type),
        }

    def layers(self, nodes: list[dict[str, object]]) -> dict[str, dict[str, object]]:
        layers: dict[str, dict[str, object]] = {}
        for tradition in TRADITIONS:
            aligned_nodes = [
                str(node["id"])
                for node in nodes
                if str(node.get("tradition") or "").lower() == tradition
                or str(node.get("tradition") or "").lower() == "shared_core"
            ]
            layers[tradition] = {
                "visible_nodes": aligned_nodes,
                "emphasis": self.tradition_emphasis(tradition),
            }
        return layers

    def visual_state(self, confidence: float) -> str:
        if confidence >= 0.8:
            return "solid"
        if confidence >= 0.5:
            return "translucent"
        return "faded"

    def edge_label(self, edge_type: str) -> str:
        labels = {
            "SEMANTIC_CONFLICT": "interpretive difference",
            "DOCTRINAL_CONFLICT": "doctrinal divergence",
            "ONTOLOGICAL_CONFLICT": "ontological conflict",
        }
        return labels.get(edge_type, edge_type.lower().replace("_", " "))

    def tradition_emphasis(self, tradition: str) -> list[str]:
        return {
            "theravada": ["impermanence", "cessation", "suffering"],
            "mahayana": ["emptiness", "non-duality", "bodhisattva"],
            "vajrayana": ["bardo", "transformation", "visualization"],
        }[tradition]
