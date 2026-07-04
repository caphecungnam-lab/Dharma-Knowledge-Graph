from __future__ import annotations

from typing import Any


class RetrievalControlLayer:
    def fetch(self, query: str, vector: Any, graph: Any) -> list[dict[str, Any]]:
        matches = vector.search(query)
        controlled_context = []
        for match in matches:
            if not self._has_valid_source(match):
                continue
            if float(match.get("score") or 0.0) < 0.5:
                continue

            node_id = str(match.get("node_id") or "")
            related = graph.related_concepts(node_id) if node_id else []
            controlled_context.append(
                {
                    "match": match,
                    "related": self._traceable_related(related),
                }
            )
        return controlled_context

    def _has_valid_source(self, match: dict[str, Any]) -> bool:
        return bool(
            match.get("source_id")
            or match.get("source_url")
            or match.get("citation_id")
            or match.get("source_type") == "sutta"
        )

    def _traceable_related(
        self,
        related_nodes: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        traceable = []
        for node in related_nodes:
            if node.get("source_id") or node.get("source_url") or node.get("id"):
                traceable.append(node)
        return traceable
