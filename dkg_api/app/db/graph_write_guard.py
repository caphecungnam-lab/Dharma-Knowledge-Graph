from __future__ import annotations

from typing import Any

from dkg_api.app.ingestion.validation_layer import validate_ingested_node


class GraphWriteGuard:
    def __init__(self, graph: Any) -> None:
        self.graph = graph

    def write_node(self, node: dict[str, Any]) -> dict[str, Any]:
        validation = validate_ingested_node(node)
        if validation["status"] != "ok":
            return {
                **validation,
                "stage": "graph_write",
            }
        if self._has_unlabeled_conflict(node):
            return {
                "status": "rejected",
                "stage": "graph_write",
                "reason": "schema_violation",
                "node_id": validation["node_id"],
                "missing": ["conflict_label"],
            }

        self.graph.upsert_generated_node(node)
        self.graph.link_source_chunk(node)
        return {
            "status": "ok",
            "node_id": validation["node_id"],
            "node": validation["node"],
        }

    def write_relationship(
        self,
        relation: dict[str, str],
        allowed_ids: set[str],
    ) -> dict[str, Any]:
        source_id = relation.get("source")
        target_id = relation.get("target")
        if source_id not in allowed_ids or target_id not in allowed_ids:
            return {
                "status": "rejected",
                "stage": "graph_write",
                "reason": "schema_violation",
                "relation": relation,
            }
        self.graph.create_relationship(
            source_id,
            target_id,
            relation.get("type") or "RELATED_TO",
        )
        return {
            "status": "ok",
            "relation": relation,
        }

    def write_contradiction(self, contradiction: dict[str, object]) -> dict[str, Any]:
        if not contradiction.get("conflict_type"):
            return {
                "status": "rejected",
                "stage": "graph_write",
                "reason": "schema_violation",
                "missing": ["conflict_type"],
            }
        self.graph.create_contradiction(contradiction)
        return {
            "status": "ok",
            "contradiction": contradiction,
        }

    def _has_unlabeled_conflict(self, node: dict[str, Any]) -> bool:
        conflict = node.get("conflict") or {}
        conflict_type = conflict.get("type")
        return bool(
            conflict_type
            and conflict_type != "none"
            and not node.get("conflict_labeled")
        )
