from __future__ import annotations

from typing import Any


class ContextSanitizer:
    def sanitize(
        self,
        context: list[dict[str, Any]],
        allowed_layers: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        allowed = set(allowed_layers or [])
        sanitized = []
        for node in context:
            if allowed and node.get("epistemic_type") not in allowed:
                continue
            if not self._is_epistemically_valid(node):
                continue
            if self._has_unresolved_ontological_conflict(node):
                continue
            sanitized.append(node)
        return sanitized

    def _is_epistemically_valid(self, node: dict[str, Any]) -> bool:
        traceability = node.get("traceability") or {}
        return bool(
            node.get("epistemic_type") != "unknown"
            and float(node.get("confidence") or 0.0) >= 0.5
            and node.get("ai_usage_allowed") is True
            and traceability.get("node_id")
            and (traceability.get("sources") or traceability.get("graph_links"))
        )

    def _has_unresolved_ontological_conflict(self, node: dict[str, Any]) -> bool:
        conflict = node.get("conflict") or {}
        return (
            conflict.get("type") == "ontological"
            and float(conflict.get("severity") or 0.0) >= 0.8
            and not node.get("conflict_labeled")
        )
