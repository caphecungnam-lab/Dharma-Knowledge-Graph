from __future__ import annotations

from typing import Any

from dkg_api.app.safety.safety_policy import normalize_epistemic_type, normalize_tradition

REQUIRED_CONCEPT_FIELDS = {
    "id",
    "label",
    "definition",
    "tradition",
    "epistemic_type",
    "source_id",
    "chunk_id",
    "confidence",
}

VALID_EPISTEMIC_TYPES = {
    "core_fact",
    "doctrinal",
    "interpretive",
    "esoteric",
    "unknown",
}


class GraphSchema:
    def concept_node(self, node: dict[str, Any]) -> dict[str, Any]:
        match = node.get("match") or {}
        traceability = node.get("traceability") or {}
        sources = list(node.get("source_ids") or traceability.get("sources") or [])
        source_id = str(node.get("source_id") or match.get("source_id") or (sources[0] if sources else "")).strip()
        chunk_id = str(node.get("chunk_id") or match.get("chunk_id") or "").strip()
        node_id = str(node.get("id") or node.get("node_id") or match.get("node_id") or "").strip()
        confidence = self._confidence(node.get("confidence", match.get("score")))

        return {
            "id": node_id,
            "label": str(node.get("label") or match.get("label") or node_id).strip(),
            "definition": str(
                node.get("definition")
                or match.get("definition")
                or match.get("text")
                or ""
            ).strip(),
            "tradition": normalize_tradition(node.get("tradition") or match.get("tradition")) or "unknown",
            "epistemic_type": normalize_epistemic_type(node.get("epistemic_type") or match.get("epistemic_type")),
            "source_id": source_id,
            "chunk_id": chunk_id,
            "confidence": confidence,
        }

    def validate_concept_node(self, node: dict[str, Any]) -> dict[str, Any]:
        normalized = self.concept_node(node)
        missing = [
            field
            for field in sorted(REQUIRED_CONCEPT_FIELDS)
            if normalized.get(field) in {None, ""}
        ]
        if missing:
            return {
                "status": "rejected",
                "reason": "schema_violation",
                "missing": missing,
                "node": normalized,
            }
        if normalized["epistemic_type"] not in VALID_EPISTEMIC_TYPES:
            return {
                "status": "rejected",
                "reason": "schema_violation",
                "missing": ["valid_epistemic_type"],
                "node": normalized,
            }
        if not 0.0 <= float(normalized["confidence"]) <= 1.0:
            return {
                "status": "rejected",
                "reason": "schema_violation",
                "missing": ["valid_confidence"],
                "node": normalized,
            }
        return {
            "status": "ok",
            "node": normalized,
        }

    def _confidence(self, value: object) -> float:
        try:
            confidence = float(value)
        except (TypeError, ValueError):
            confidence = 0.0
        return round(max(0.0, min(confidence, 1.0)), 3)
