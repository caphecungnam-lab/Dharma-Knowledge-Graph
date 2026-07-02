#!/usr/bin/env python3
"""Validate JSON seed files for the Dharma Knowledge Graph."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEED_DIR = ROOT / "data" / "seeds"
REQUIRED_NODE_FIELDS = {"id", "type", "name"}
REQUIRED_RELATIONSHIP_FIELDS = {"source", "type", "target"}


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
            if isinstance(node_id, str):
                if node_id in node_locations:
                    errors.append(
                        f"{path}: duplicate node id: {node_id} "
                        f"(already in {node_locations[node_id]})"
                    )
                node_locations[node_id] = path
            else:
                errors.append(f"{path}: node {index} has non-string id")

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
