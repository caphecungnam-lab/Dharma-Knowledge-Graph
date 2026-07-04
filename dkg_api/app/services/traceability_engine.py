from __future__ import annotations

from typing import Any


class TraceabilityEngine:
    def attach(self, node: dict[str, Any]) -> dict[str, object]:
        match = node.get("match", {})
        node_id = str(match.get("node_id") or "")
        sources = self._sources(node)
        graph_links = self._graph_links(node)

        return {
            "node_id": node_id,
            "sources": sources,
            "graph_links": graph_links,
        }

    def has_trace(self, traceability: dict[str, object]) -> bool:
        return bool(
            traceability.get("node_id")
            and (traceability.get("sources") or traceability.get("graph_links"))
        )

    def _sources(self, node: dict[str, Any]) -> list[str]:
        match = node.get("match", {})
        source_values = [
            match.get("source_id"),
            match.get("source_url"),
            match.get("citation_id"),
        ]
        for related in node.get("related", []):
            source_values.extend(
                [
                    related.get("source_id"),
                    related.get("source_url"),
                    related.get("citation_id"),
                ]
            )

        sources = []
        for value in source_values:
            text = str(value or "").strip()
            if text and text not in sources:
                sources.append(text)
        return sources

    def _graph_links(self, node: dict[str, Any]) -> list[str]:
        match = node.get("match", {})
        node_id = str(match.get("node_id") or "")
        links = []
        for related in node.get("related", []):
            related_id = str(related.get("id") or "").strip()
            if node_id and related_id:
                links.append(f"{node_id}->RELATED_TO->{related_id}")
        return links
