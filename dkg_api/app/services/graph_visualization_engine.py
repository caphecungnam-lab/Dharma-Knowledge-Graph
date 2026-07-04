from __future__ import annotations

from typing import Any

from dkg_api.app.services.epistemic_ui_adapter import EpistemicUIAdapter
from dkg_api.app.services.knowledge_map_builder import KnowledgeMapBuilder
from dkg_api.app.services.tradition_overlay_engine import TraditionOverlayEngine


class GraphVisualizationEngine:
    def __init__(self) -> None:
        self.adapter = EpistemicUIAdapter()
        self.map_builder = KnowledgeMapBuilder()
        self.overlay_engine = TraditionOverlayEngine()

    def build_map(
        self,
        concept_id: str,
        graph_data: dict[str, Any],
    ) -> dict[str, object]:
        raw_nodes = graph_data.get("nodes", [])
        raw_edges = graph_data.get("edges", [])
        nodes = [
            self.adapter.node(raw_node, index, len(raw_nodes))
            for index, raw_node in enumerate(raw_nodes)
        ]
        edges = [self.adapter.edge(raw_edge) for raw_edge in raw_edges]
        return {
            "map_id": f"map_{concept_id}",
            "center_node": concept_id,
            "nodes": nodes,
            "edges": edges,
            "clusters": self.map_builder.build_clusters(concept_id, nodes),
            "layers": self.adapter.layers(nodes),
        }

    def build_overlay(
        self,
        concept_id: str,
        graph_data: dict[str, Any],
    ) -> dict[str, object]:
        knowledge_map = self.build_map(concept_id, graph_data)
        return {
            "concept_id": concept_id,
            "layers": self.overlay_engine.build_overlay(
                concept_id,
                knowledge_map["nodes"],
                knowledge_map["edges"],
            ),
        }

    def build_clusters(
        self,
        concept_id: str,
        graph_data: dict[str, Any],
    ) -> dict[str, object]:
        knowledge_map = self.build_map(concept_id, graph_data)
        return {
            "concept_id": concept_id,
            "clusters": knowledge_map["clusters"],
        }
