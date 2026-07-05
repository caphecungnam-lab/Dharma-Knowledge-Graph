from __future__ import annotations

from typing import Any

from dkg_api.app.schemas.graph_schema import GraphSchema


def validate_ingested_node(node: dict[str, Any]) -> dict[str, Any]:
    schema = GraphSchema()
    schema_result = schema.validate_concept_node(node)
    normalized = schema_result.get("node", {})
    if schema_result["status"] != "ok":
        if "source_id" in schema_result.get("missing", []):
            return {
                "status": "rejected",
                "reason": "missing_source",
                "node_id": normalized.get("id"),
                "node": normalized,
            }
        return {
            "status": "rejected",
            "reason": "schema_violation",
            "node_id": normalized.get("id"),
            "node": normalized,
        }

    if _is_inferred(node):
        return {
            "status": "rejected",
            "reason": "schema_violation",
            "node_id": normalized["id"],
            "node": normalized,
        }
    if not normalized.get("source_id"):
        return {
            "status": "rejected",
            "reason": "missing_source",
            "node_id": normalized["id"],
            "node": normalized,
        }
    if float(normalized["confidence"]) < 0.5:
        return {
            "status": "rejected",
            "reason": "low_confidence",
            "node_id": normalized["id"],
            "node": normalized,
        }
    if normalized["epistemic_type"] == "unknown":
        return {
            "status": "rejected",
            "reason": "schema_violation",
            "node_id": normalized["id"],
            "node": normalized,
        }
    return {
        "status": "ok",
        "node_id": normalized["id"],
        "node": normalized,
    }


def _is_inferred(node: dict[str, Any]) -> bool:
    match = node.get("match") or {}
    return bool(
        node.get("inferred")
        or match.get("inferred")
        or node.get("generated_doctrine")
        or match.get("generated_doctrine")
    )
