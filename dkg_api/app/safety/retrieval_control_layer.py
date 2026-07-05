from __future__ import annotations

from typing import Any


class RetrievalControlLayer:
    def fetch(self, query: str, vector: Any, graph: Any) -> list[dict[str, Any]]:
        try:
            matches = vector.search(query)
        except Exception:
            return self._graph_only(query, graph)

        controlled_context = []
        for match in matches:
            if not self._has_valid_source(match):
                continue
            if float(match.get("score") or 0.0) < 0.5:
                continue

            node_id = str(match.get("node_id") or "")
            try:
                related = graph.related_concepts(node_id) if node_id else []
            except Exception:
                related = []
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

    def _graph_only(self, query: str, graph: Any) -> list[dict[str, Any]]:
        try:
            matches = graph.search_concepts(query)
        except Exception:
            return []

        controlled_context = []
        for match in matches:
            if self._has_valid_source(match):
                controlled_context.append({"match": match, "related": []})
        return controlled_context
