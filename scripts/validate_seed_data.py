#!/usr/bin/env python3
"""Validate JSON seed files for the Dharma Knowledge Graph."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEED_DIR = ROOT / "data" / "seeds"
REQUIRED_NODE_FIELDS = {"id", "type", "name"}
REQUIRED_RELATIONSHIP_FIELDS = {"source", "type", "target"}
ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
TYPE_PREFIXES = {
    "Citation": "citation_",
    "Concept": "concept_",
    "Corpus": "corpus_",
    "Document": "document_",
    "Evidence": "evidence_",
    "Person": "person_",
    "Place": "place_",
    "School": "school_",
    "Source": "source_",
    "Term": "term_",
    "Text": "text_",
    "Work": "work_",
}
KNOWN_NODE_TYPES = set(TYPE_PREFIXES)
RELATIONSHIP_TYPE_RULES = {
    "AUTHORED_BY": ({"Text"}, {"Person"}),
    "BELONGS_TO_SCHOOL": ({"Concept", "Person", "School", "Text"}, {"School"}),
    "BELONGS_TO_CORPUS": (
        {"Citation", "Document", "Evidence", "Source", "Work"},
        {"Corpus"},
    ),
    "CITES": ({"Citation", "Text"}, {"Citation"}),
    "COMMENTS_ON": ({"Citation", "Text"}, {"Concept", "Text"}),
    "DEFINES": ({"Citation", "Concept", "Term", "Text"}, {"Concept", "Term"}),
    "DERIVED_FROM": (
        {"Citation", "Document", "Evidence", "Work"},
        {"Citation", "Document", "Source", "Work"},
    ),
    "EVIDENCES": ({"Evidence"}, {"Concept", "Term", "Text", "Work"}),
    "HAS_CITATION": ({"Document", "Evidence", "Text", "Work"}, {"Citation"}),
    "HAS_DOCUMENT": ({"Corpus", "Source", "Work"}, {"Document"}),
    "HAS_EVIDENCE": ({"Citation", "Document", "Work"}, {"Evidence"}),
    "LOCATED_IN": ({"Person", "Place", "School", "Text"}, {"Place"}),
    "MENTIONS": (
        {"Citation", "Concept", "Document", "Evidence", "Text", "Work"},
        {"Concept", "Person", "Place", "School", "Term", "Text", "Work"},
    ),
    "RELATED_TO": (KNOWN_NODE_TYPES, KNOWN_NODE_TYPES),
    "TRANSLATED_BY": ({"Text"}, {"Person"}),
}
REQUIRED_EVIDENCE_FIELDS = {
    "evidence_text",
    "evidence_type",
    "confidence",
    "review_status",
}
ALLOWED_EVIDENCE_TYPES = {
    "transcript_excerpt",
    "citation_excerpt",
    "paraphrase",
    "ai_summary",
    "human_note",
}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}
ALLOWED_REVIEW_STATUS = {
    "unreviewed",
    "ai_processed",
    "human_reviewed",
    "verified",
}


def is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and value.strip() != ""


def missing_or_empty_string(node: dict, field: str) -> bool:
    value = node.get(field)
    return not is_non_empty_string(value)


def validate_evidence_node(path: Path, index: int, node: dict) -> list[str]:
    errors: list[str] = []

    for field in sorted(REQUIRED_EVIDENCE_FIELDS):
        if missing_or_empty_string(node, field):
            errors.append(
                f"{path}: node {index} Evidence missing required field: {field}"
            )

    evidence_type = node.get("evidence_type")
    if is_non_empty_string(evidence_type) and evidence_type not in ALLOWED_EVIDENCE_TYPES:
        errors.append(
            f"{path}: node {index} Evidence has invalid evidence_type: "
            f"{evidence_type}"
        )

    confidence = node.get("confidence")
    if is_non_empty_string(confidence) and confidence not in ALLOWED_CONFIDENCE:
        errors.append(
            f"{path}: node {index} Evidence has invalid confidence: {confidence}"
        )

    review_status = node.get("review_status")
    if is_non_empty_string(review_status) and review_status not in ALLOWED_REVIEW_STATUS:
        errors.append(
            f"{path}: node {index} Evidence has invalid review_status: "
            f"{review_status}"
        )

    if evidence_type == "transcript_excerpt" and missing_or_empty_string(node, "speaker"):
        errors.append(
            f"{path}: node {index} Evidence with transcript_excerpt "
            "requires speaker"
        )

    if node.get("source_kind") == "youtube" and missing_or_empty_string(node, "source_url"):
        errors.append(
            f"{path}: node {index} Evidence with source_kind youtube "
            "requires source_url"
        )

    return errors


def load_seed_file(path: Path) -> tuple[dict, list[str]]:
    errors: list[str] = []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {}, [f"{path}: invalid JSON: {exc}"]

    nodes = data.get("nodes")
    relationships = data.get("relationships")

    if not isinstance(nodes, list):
        errors.append(f"{path}: 'nodes' must be a list")
        nodes = []

    if not isinstance(relationships, list):
        errors.append(f"{path}: 'relationships' must be a list")

    return data, errors


def validate_seed_files(seed_files: list[Path]) -> list[str]:
    errors: list[str] = []
    loaded_files: list[tuple[Path, dict]] = []
    node_locations: dict[str, Path] = {}
    node_types: dict[str, str] = {}
    relationship_locations: dict[tuple[str, str, str], Path] = {}

    for path in seed_files:
        data, load_errors = load_seed_file(path)
        errors.extend(load_errors)
        if data:
            loaded_files.append((path, data))

    for path, data in loaded_files:
        for index, node in enumerate(data.get("nodes", [])):
            if not isinstance(node, dict):
                errors.append(f"{path}: node {index} must be an object")
                continue

            missing = REQUIRED_NODE_FIELDS - node.keys()
            if missing:
                errors.append(f"{path}: node {index} missing fields: {sorted(missing)}")

            node_id = node.get("id")
            node_type = node.get("type")
            if isinstance(node_id, str):
                if not ID_PATTERN.match(node_id):
                    errors.append(
                        f"{path}: node {index} has invalid id format: {node_id}"
                    )
                if isinstance(node_type, str) and node_type in TYPE_PREFIXES:
                    expected_prefix = TYPE_PREFIXES[node_type]
                    if not node_id.startswith(expected_prefix):
                        errors.append(
                            f"{path}: node {index} id should start with "
                            f"'{expected_prefix}' for type '{node_type}': {node_id}"
                        )
                if node_id in node_locations:
                    errors.append(
                        f"{path}: duplicate node id: {node_id} "
                        f"(already in {node_locations[node_id]})"
                    )
                node_locations[node_id] = path
                if isinstance(node_type, str):
                    node_types[node_id] = node_type
            else:
                errors.append(f"{path}: node {index} has non-string id")

            if not isinstance(node_type, str):
                errors.append(f"{path}: node {index} has non-string type")
            elif node_type not in TYPE_PREFIXES:
                errors.append(f"{path}: node {index} has unknown type: {node_type}")
            elif node_type == "Evidence":
                errors.extend(validate_evidence_node(path, index, node))

    for path, data in loaded_files:
        for index, relationship in enumerate(data.get("relationships", [])):
            if not isinstance(relationship, dict):
                errors.append(f"{path}: relationship {index} must be an object")
                continue

            missing = REQUIRED_RELATIONSHIP_FIELDS - relationship.keys()
            if missing:
                errors.append(
                    f"{path}: relationship {index} missing fields: {sorted(missing)}"
                )
                continue

            source = relationship["source"]
            relationship_type = relationship["type"]
            target = relationship["target"]
            if source not in node_locations:
                errors.append(f"{path}: relationship {index} has unknown source: {source}")
            if target not in node_locations:
                errors.append(f"{path}: relationship {index} has unknown target: {target}")

            if not isinstance(relationship_type, str):
                errors.append(f"{path}: relationship {index} has non-string type")
                continue

            if relationship_type not in RELATIONSHIP_TYPE_RULES:
                errors.append(
                    f"{path}: relationship {index} has unknown type: "
                    f"{relationship_type}"
                )
                continue

            relationship_key = (source, relationship_type, target)
            if relationship_key in relationship_locations:
                errors.append(
                    f"{path}: duplicate relationship {relationship_key} "
                    f"(already in {relationship_locations[relationship_key]})"
                )
            relationship_locations[relationship_key] = path

            if source not in node_types or target not in node_types:
                continue

            allowed_source_types, allowed_target_types = RELATIONSHIP_TYPE_RULES[
                relationship_type
            ]
            source_type = node_types[source]
            target_type = node_types[target]
            if source_type not in allowed_source_types:
                errors.append(
                    f"{path}: relationship {index} type '{relationship_type}' "
                    f"does not allow source type '{source_type}'"
                )
            if target_type not in allowed_target_types:
                errors.append(
                    f"{path}: relationship {index} type '{relationship_type}' "
                    f"does not allow target type '{target_type}'"
                )

    return errors


def main() -> int:
    seed_files = sorted(SEED_DIR.glob("*.json"))
    if not seed_files:
        print("No seed files found.")
        return 1

    errors = validate_seed_files(seed_files)

    if errors:
        print("Seed data validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(seed_files)} seed file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
