from __future__ import annotations

from typing import Any


EPISTEMIC_PRIORITY = {
    "core_fact": 0,
    "doctrinal": 1,
    "interpretive": 2,
    "esoteric": 3,
}


class ContextReductionEngine:
    def reduce(
        self,
        context: list[dict[str, Any]],
        max_nodes: int = 8,
    ) -> list[dict[str, Any]]:
        deduped = self._dedupe(context)
        ranked = sorted(
            deduped,
            key=lambda node: (
                EPISTEMIC_PRIORITY.get(str(node.get("epistemic_type")), 9),
                -float(node.get("confidence") or 0.0),
                str(node.get("node_id") or ""),
            ),
        )
        return [self._compact(node) for node in ranked[:max_nodes]]

    def _dedupe(self, context: list[dict[str, Any]]) -> list[dict[str, Any]]:
        seen = set()
        deduped = []
        for node in context:
            match = node.get("match") or {}
            key = (
                str(match.get("text") or "").strip().lower(),
                str(node.get("node_id") or ""),
            )
            if key in seen:
                continue
            seen.add(key)
            deduped.append(node)
        return deduped

    def _compact(self, node: dict[str, Any]) -> dict[str, Any]:
        compact = dict(node)
        related = compact.get("related") or []
        compact["related"] = related[:3]
        return compact
