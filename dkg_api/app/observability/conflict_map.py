from __future__ import annotations

from collections import defaultdict
from typing import Any


class ConflictMap:
    def build(self, nodes: list[dict[str, Any]]) -> dict[str, object]:
        by_concept: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for node in nodes:
            node_id = str(node.get("node_id") or "")
            if node_id:
                by_concept[node_id].append(node)

        map_nodes = []
        edges = []
        for concept, group in by_concept.items():
            traditions = {
                str(node.get("tradition") or "unknown")
                for node in group
            }
            if len(group) < 2 and not self._has_conflict(group):
                continue

            for node in group:
                map_nodes.append(
                    {
                        "id": self._visual_node_id(node),
                        "concept": concept,
                        "tradition": str(node.get("tradition") or "unknown"),
                        "epistemic_type": str(node.get("epistemic_type") or "unknown"),
                        "confidence": float(node.get("confidence") or 0.0),
                    }
                )

            if len(traditions) > 1:
                for index, source in enumerate(group):
                    for target in group[index + 1 :]:
                        edges.append(
                            {
                                "from": self._visual_node_id(source),
                                "to": self._visual_node_id(target),
                                "label": self._edge_label(source, target),
                            }
                        )

        return {
            "nodes": map_nodes,
            "edges": edges,
            "conflict_count": len(edges),
        }

    def build_from_report(self, report: dict[str, Any]) -> dict[str, object]:
        nodes = []
        for document in report.get("documents", []):
            nodes.extend(document.get("accepted_nodes", []))
        return self.build(nodes)

    def _has_conflict(self, group: list[dict[str, Any]]) -> bool:
        return any(
            (node.get("conflict") or {}).get("type") not in {None, "", "none"}
            for node in group
        )

    def _visual_node_id(self, node: dict[str, Any]) -> str:
        return ":".join(
            [
                str(node.get("node_id") or "unknown"),
                str(node.get("tradition") or "unknown"),
                str((node.get("match") or {}).get("chunk_id") or "chunk"),
            ]
        )

    def _edge_label(self, source: dict[str, Any], target: dict[str, Any]) -> str:
        source_type = str(source.get("epistemic_type") or "")
        target_type = str(target.get("epistemic_type") or "")
        if source_type != target_type:
            return "DOCTRINAL_VARIATION"
        if source.get("tradition") != target.get("tradition"):
            return "INTERPRETS_DIFFERENTLY"
        return "CONTRADICTS"
