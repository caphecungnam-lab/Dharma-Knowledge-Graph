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
    "Person": "person_",
    "Place": "place_",
    "School": "school_",
    "Term": "term_",
    "Text": "text_",
}


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
            else:
                errors.append(f"{path}: node {index} has non-string id")

            if isinstance(node_type, str) and node_type not in TYPE_PREFIXES:
                errors.append(f"{path}: node {index} has unknown type: {node_type}")

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
            target = relationship["target"]
            if source not in node_locations:
                errors.append(f"{path}: relationship {index} has unknown source: {source}")
            if target not in node_locations:
                errors.append(f"{path}: relationship {index} has unknown target: {target}")

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
