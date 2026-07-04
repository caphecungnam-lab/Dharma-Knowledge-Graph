from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

if TYPE_CHECKING:
    from dkg_api.app.services.graph_service import GraphService


class GraphExpander:
    def __init__(self, graph: GraphService) -> None:
        self.graph = graph

    def expand(
        self,
        validated_nodes: list[dict[str, Any]],
        relations: list[dict[str, str]] | None = None,
        contradictions: list[dict[str, object]] | None = None,
    ) -> dict[str, object]:
        inserted_nodes = []
        relations = relations or []
        contradictions = contradictions or []
        allowed_ids = {
            str(node.get("node_id"))
            for node in validated_nodes
            if node.get("ai_usage_allowed") is True
        }

        for node in validated_nodes:
            if node.get("ai_usage_allowed") is not True:
                continue
            self.graph.upsert_generated_node(node)
            self.graph.link_source_chunk(node)
            inserted_nodes.append(node["node_id"])

        inserted_relations = []
        for relation in relations:
            if (
                relation["source"] not in allowed_ids
                or relation["target"] not in allowed_ids
            ):
                continue
            self.graph.create_relationship(
                relation["source"],
                relation["target"],
                relation["type"],
            )
            inserted_relations.append(relation)

        for contradiction in contradictions:
            self.graph.create_contradiction(contradiction)

        return {
            "inserted_nodes": inserted_nodes,
            "inserted_relations": inserted_relations,
            "contradictions": contradictions,
        }
