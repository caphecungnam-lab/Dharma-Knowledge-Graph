from __future__ import annotations

from typing import Any

from dkg_api.app.safety.safety_policy import (
    normalize_epistemic_type,
    normalize_tradition,
)


class ContextSanitizer:
    def sanitize(
        self,
        context: list[dict[str, Any]],
        allowed_layers: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        allowed = set(allowed_layers or [])
        sanitized = []
        for node in context:
            normalized_node = self._normalize_node(node)
            if normalized_node is None:
                continue
            if allowed and normalized_node.get("epistemic_type") not in allowed:
                continue
            if not self._is_epistemically_valid(normalized_node):
                continue
            if self._has_unresolved_ontological_conflict(normalized_node):
                continue
            sanitized.append(normalized_node)
        return sanitized

    def _is_epistemically_valid(self, node: dict[str, Any]) -> bool:
        traceability = node.get("traceability") or {}
        return bool(
            node.get("epistemic_type") != "unknown"
            and float(node.get("confidence") or 0.0) >= 0.5
            and node.get("ai_usage_allowed") is True
            and traceability.get("node_id")
            and node.get("source_ids")
        )

    def _has_unresolved_ontological_conflict(self, node: dict[str, Any]) -> bool:
        conflict = node.get("conflict") or {}
        return (
            conflict.get("type") == "ontological"
            and float(conflict.get("severity") or 0.0) >= 0.8
            and not node.get("conflict_labeled")
        )

    def _normalize_node(self, node: dict[str, Any]) -> dict[str, Any] | None:
        traceability = dict(node.get("traceability") or {})
        match = node.get("match") or {}
        node_id = str(node.get("node_id") or traceability.get("node_id") or "").strip()
        source_ids = self._source_ids(node, traceability)
        tradition = normalize_tradition(node.get("tradition") or match.get("tradition"))
        if not node_id or not source_ids or tradition is None:
            return None

        normalized = dict(node)
        normalized["node_id"] = node_id
        normalized["epistemic_type"] = normalize_epistemic_type(
            node.get("epistemic_type")
        )
        normalized["confidence"] = self._bounded_confidence(node.get("confidence"))
        normalized["source_ids"] = source_ids
        normalized["tradition"] = tradition
        traceability["node_id"] = node_id
        traceability["sources"] = source_ids
        normalized["traceability"] = traceability
        return normalized

    def _source_ids(
        self,
        node: dict[str, Any],
        traceability: dict[str, Any],
    ) -> list[str]:
        values = list(node.get("source_ids") or [])
        values.extend(traceability.get("sources") or [])
        source_ids = []
        for value in values:
            text = str(value or "").strip()
            if text and text not in source_ids:
                source_ids.append(text)
        return source_ids

    def _bounded_confidence(self, value: object) -> float:
        confidence = float(value or 0.0)
        return round(max(0.0, min(confidence, 1.0)), 3)
