#!/usr/bin/env python3
"""Export processed graph data to Neo4j-friendly CSV files."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = ROOT / "data" / "processed" / "graph.json"
NEO4J_DIR = ROOT / "data" / "processed" / "neo4j"
DOCS_NEO4J_DIR = ROOT / "docs" / "artifacts" / "neo4j"


NODE_FIELDS = [
    "id:ID",
    ":LABEL",
    "name",
    "description",
    "category",
    "pali",
    "sanskrit",
    "tradition",
    "language",
    "source",
    "locator",
    "url",
    "notes",
    "scope",
    "source_type",
    "document_type",
    "evidence_type",
    "evidence_text",
    "confidence",
    "source_file",
]
RELATIONSHIP_FIELDS = [
    ":START_ID",
    ":TYPE",
    ":END_ID",
    "source_file",
]


def load_graph() -> dict:
    if not GRAPH_PATH.exists():
        raise FileNotFoundError(
            f"{GRAPH_PATH.relative_to(ROOT)} does not exist. "
            "Run scripts/build_graph.py first."
        )
    return json.loads(GRAPH_PATH.read_text(encoding="utf-8"))


def write_nodes(nodes: list[dict], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=NODE_FIELDS, lineterminator="\n")
        writer.writeheader()

        for node in nodes:
            writer.writerow(
                {
                    "id:ID": node["id"],
                    ":LABEL": node["type"],
                    "name": node["name"],
                    "description": node.get("description", ""),
                    "category": node.get("category", ""),
                    "pali": node.get("pali", ""),
                    "sanskrit": node.get("sanskrit", ""),
                    "tradition": node.get("tradition", ""),
                    "language": node.get("language", ""),
                    "source": node.get("source", ""),
                    "locator": node.get("locator", ""),
                    "url": node.get("url", ""),
                    "notes": node.get("notes", ""),
                    "scope": node.get("scope", ""),
                    "source_type": node.get("source_type", ""),
                    "document_type": node.get("document_type", ""),
                    "evidence_type": node.get("evidence_type", ""),
                    "evidence_text": node.get("evidence_text", ""),
                    "confidence": node.get("confidence", ""),
                    "source_file": node.get("source_file", ""),
                }
            )


def write_relationships(relationships: list[dict], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=RELATIONSHIP_FIELDS, lineterminator="\n")
        writer.writeheader()

        for relationship in relationships:
            writer.writerow(
                {
                    ":START_ID": relationship["source"],
                    ":TYPE": relationship["type"],
                    ":END_ID": relationship["target"],
                    "source_file": relationship.get("source_file", ""),
                }
            )


def main() -> int:
    graph = load_graph()
    NEO4J_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_NEO4J_DIR.mkdir(parents=True, exist_ok=True)

    output_dirs = [NEO4J_DIR, DOCS_NEO4J_DIR]
    for output_dir in output_dirs:
        write_nodes(graph["nodes"], output_dir / "nodes.csv")
        write_relationships(graph["relationships"], output_dir / "relationships.csv")
        print(f"Wrote {output_dir.relative_to(ROOT)}/nodes.csv")
        print(f"Wrote {output_dir.relative_to(ROOT)}/relationships.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
