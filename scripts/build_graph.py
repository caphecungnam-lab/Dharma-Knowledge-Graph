#!/usr/bin/env python3
"""Build processed graph artifacts from seed data."""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEED_DIR = ROOT / "data" / "seeds"
PROCESSED_DIR = ROOT / "data" / "processed"
EXPLORER_DIR = ROOT / "docs" / "graph-explorer"


def read_seed_files() -> list[tuple[Path, dict]]:
    seed_files = sorted(SEED_DIR.glob("*.json"))
    return [
        (path, json.loads(path.read_text(encoding="utf-8")))
        for path in seed_files
    ]


def build_graph() -> dict:
    nodes: dict[str, dict] = {}
    relationships: list[dict] = []
    source_files: list[str] = []

    for path, data in read_seed_files():
        source_files.append(str(path.relative_to(ROOT)))

        for node in data["nodes"]:
            enriched_node = dict(node)
            enriched_node["source_file"] = str(path.relative_to(ROOT))
            nodes[enriched_node["id"]] = enriched_node

        for relationship in data["relationships"]:
            enriched_relationship = dict(relationship)
            enriched_relationship["source_file"] = str(path.relative_to(ROOT))
            relationships.append(enriched_relationship)

    node_list = sorted(nodes.values(), key=lambda node: (node["type"], node["name"]))
    relationship_list = sorted(
        relationships,
        key=lambda rel: (rel["type"], rel["source"], rel["target"]),
    )

    node_type_counts = Counter(node["type"] for node in node_list)
    relationship_type_counts = Counter(rel["type"] for rel in relationship_list)

    return {
        "metadata": {
            "title": "Dharma Knowledge Graph",
            "version": "0.1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_files": source_files,
        },
        "summary": {
            "node_count": len(node_list),
            "relationship_count": len(relationship_list),
            "node_type_counts": dict(sorted(node_type_counts.items())),
            "relationship_type_counts": dict(sorted(relationship_type_counts.items())),
        },
        "nodes": node_list,
        "relationships": relationship_list,
    }


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_explorer_data(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    graph_json = json.dumps(data, indent=2, ensure_ascii=False)
    path.write_text(f"window.DHARMA_GRAPH = {graph_json};\n", encoding="utf-8")


def main() -> int:
    graph = build_graph()
    graph_json_path = PROCESSED_DIR / "graph.json"
    graph_data_path = EXPLORER_DIR / "graph-data.js"

    write_json(graph_json_path, graph)
    write_explorer_data(graph_data_path, graph)

    print(f"Wrote {graph_json_path.relative_to(ROOT)}")
    print(f"Wrote {graph_data_path.relative_to(ROOT)}")
    print(
        f"Graph has {graph['summary']['node_count']} nodes and "
        f"{graph['summary']['relationship_count']} relationships."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
