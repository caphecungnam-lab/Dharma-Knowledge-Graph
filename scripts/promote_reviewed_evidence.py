#!/usr/bin/env python3
"""Promote human-reviewed Evidence into curated corpus data."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

VIDEO_ID = "FISpARohzy8"
CITATION_ID = "citation_youtube_fisp_arohzy8"
CURATED_AT = "2026-07-03"
CURATOR = "Minh"
DEFAULT_INPUT_PATH = (
    Path("data") / "reviewed" / "giac_khang" / VIDEO_ID / "evidence_review_queue.json"
)
DEFAULT_OUTPUT_PATH = (
    Path("data") / "curated" / "giac_khang" / VIDEO_ID / "evidence_curated.json"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def is_promotable_evidence(node: dict[str, Any]) -> bool:
    return (
        node.get("type") == "Evidence" and node.get("review_status") == "human_reviewed"
    )


def build_curated_evidence_node(node: dict[str, Any]) -> dict[str, Any]:
    curated_node = deepcopy(node)
    reviewed_text = str(node.get("reviewed_evidence_text", ""))

    curated_node["evidence_text"] = reviewed_text
    curated_node["curated_status"] = "curated"
    curated_node["curated_at"] = CURATED_AT
    curated_node["curator"] = CURATOR

    return curated_node


def relationship_key(relationship: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(relationship.get("source", "")),
        str(relationship.get("type", "")),
        str(relationship.get("target", "")),
    )


def is_source_reference_node(node: dict[str, Any]) -> bool:
    return node.get("type") in {"Citation", "Document", "Source"}


def is_source_reference_id(node_id: str) -> bool:
    return node_id.startswith(("citation_", "document_", "source_"))


def should_preserve_relationship(
    relationship: dict[str, Any],
    promoted_node_ids: set[str],
    existing_node_ids: set[str],
    source_reference_ids: set[str],
) -> bool:
    source = str(relationship.get("source", ""))
    target = str(relationship.get("target", ""))

    if source not in promoted_node_ids:
        return False

    if target in promoted_node_ids:
        return True

    if target in existing_node_ids and target in source_reference_ids:
        return True

    return is_source_reference_id(target)


def default_relationships_for_node(node: dict[str, Any]) -> list[dict[str, str]]:
    relationships = [
        {
            "source": node["id"],
            "type": "HAS_CITATION",
            "target": CITATION_ID,
        }
    ]

    document_id = node.get("document_id")
    if document_id:
        relationships.append(
            {
                "source": node["id"],
                "type": "DERIVED_FROM",
                "target": str(document_id),
            }
        )

    return relationships


def build_curated_relationships(
    source_payload: dict[str, Any],
    promoted_node_ids: set[str],
    promoted_nodes: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    relationships: dict[tuple[str, str, str], dict[str, Any]] = {}
    source_nodes = [
        node for node in source_payload.get("nodes", []) if isinstance(node, dict)
    ]
    existing_node_ids = {str(node.get("id", "")) for node in source_nodes}
    source_reference_ids = {
        str(node.get("id", ""))
        for node in source_nodes
        if is_source_reference_node(node)
    }

    for relationship in source_payload.get("relationships", []):
        if should_preserve_relationship(
            relationship,
            promoted_node_ids,
            existing_node_ids,
            source_reference_ids,
        ):
            relationships[relationship_key(relationship)] = deepcopy(relationship)

    for node in promoted_nodes:
        for relationship in default_relationships_for_node(node):
            relationships.setdefault(relationship_key(relationship), relationship)

    return sorted(
        relationships.values(),
        key=lambda relationship: (
            relationship["type"],
            relationship["source"],
            relationship["target"],
        ),
    )


def promote_reviewed_evidence(source_payload: dict[str, Any]) -> dict[str, Any]:
    curated_nodes = [
        build_curated_evidence_node(node)
        for node in source_payload.get("nodes", [])
        if isinstance(node, dict) and is_promotable_evidence(node)
    ]
    promoted_node_ids = {node["id"] for node in curated_nodes}

    return {
        "nodes": curated_nodes,
        "relationships": build_curated_relationships(
            source_payload,
            promoted_node_ids,
            curated_nodes,
        ),
    }


def promote_reviewed_evidence_file(
    input_path: Path = DEFAULT_INPUT_PATH,
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> dict[str, Any]:
    source_payload = load_json(input_path)
    curated_payload = promote_reviewed_evidence(source_payload)
    write_json(output_path, curated_payload)
    return curated_payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Promote human-reviewed Evidence into curated corpus data."
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="Input reviewed Evidence queue JSON file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Output curated Evidence JSON file.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    curated_payload = promote_reviewed_evidence_file(args.input, args.output)
    print(f"Wrote {args.output} with {len(curated_payload['nodes'])} Evidence node(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
