from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from dkg_api.app.db.graph_write_guard import GraphWriteGuard

if TYPE_CHECKING:
    from dkg_api.app.services.graph_service import GraphService


class GraphExpander:
    def __init__(self, graph: GraphService) -> None:
        self.graph = graph
        self.guard = GraphWriteGuard(graph)

    def expand(
        self,
        validated_nodes: list[dict[str, Any]],
        relations: list[dict[str, str]] | None = None,
        contradictions: list[dict[str, object]] | None = None,
    ) -> dict[str, object]:
        inserted_nodes = []
        rejected_writes = []
        relations = relations or []
        contradictions = contradictions or []
        allowed_ids = {
            str(node.get("node_id"))
            for node in validated_nodes
            if node.get("ai_usage_allowed") is True
        }
        written_ids = set()

        for node in validated_nodes:
            if node.get("ai_usage_allowed") is not True:
                continue
            if node.get("node_id") in written_ids:
                continue
            write_result = self.guard.write_node(node)
            if write_result["status"] != "ok":
                rejected_writes.append(write_result)
                continue
            written_ids.add(write_result["node_id"])
            inserted_nodes.append(write_result["node_id"])

        inserted_relations = []
        for relation in relations:
            if (
                relation["source"] not in allowed_ids
                or relation["target"] not in allowed_ids
            ):
                continue
            write_result = self.guard.write_relationship(relation, allowed_ids)
            if write_result["status"] == "ok":
                inserted_relations.append(relation)
            else:
                rejected_writes.append(write_result)

        for contradiction in contradictions:
            write_result = self.guard.write_contradiction(contradiction)
            if write_result["status"] != "ok":
                rejected_writes.append(write_result)

        return {
            "inserted_nodes": inserted_nodes,
            "inserted_relations": inserted_relations,
            "contradictions": contradictions,
            "rejected_writes": rejected_writes,
        }
