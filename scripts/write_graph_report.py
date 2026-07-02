#!/usr/bin/env python3
"""Write a Markdown report for the processed Dharma graph."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = ROOT / "data" / "processed" / "graph.json"
REPORT_PATH = ROOT / "docs" / "reports" / "graph-summary.md"


def load_graph() -> dict:
    if not GRAPH_PATH.exists():
        raise FileNotFoundError(
            f"{GRAPH_PATH.relative_to(ROOT)} does not exist. "
            "Run scripts/build_graph.py first."
        )
    return json.loads(GRAPH_PATH.read_text(encoding="utf-8"))


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def build_report(graph: dict) -> str:
    nodes = graph["nodes"]
    relationships = graph["relationships"]
    node_by_id = {node["id"]: node for node in nodes}
    degree = Counter()
    outgoing = defaultdict(list)
    incoming = defaultdict(list)

    for relationship in relationships:
        degree[relationship["source"]] += 1
        degree[relationship["target"]] += 1
        outgoing[relationship["source"]].append(relationship)
        incoming[relationship["target"]].append(relationship)

    top_connected = degree.most_common(10)
    isolated = [node for node in nodes if degree[node["id"]] == 0]

    node_type_rows = [
        [node_type, str(count)]
        for node_type, count in graph["summary"]["node_type_counts"].items()
    ]
    relationship_type_rows = [
        [relationship_type, str(count)]
        for relationship_type, count in graph["summary"][
            "relationship_type_counts"
        ].items()
    ]
    connected_rows = [
        [
            node_by_id[node_id]["name"],
            node_by_id[node_id]["type"],
            str(count),
        ]
        for node_id, count in top_connected
    ]
    isolated_rows = [
        [node["name"], node["type"], node["id"]]
        for node in isolated
    ]

    lines = [
        "# Graph Summary",
        "",
        "Generated from `data/processed/graph.json`.",
        "",
        "## Overview",
        "",
        markdown_table(
            ["Metric", "Value"],
            [
                ["Nodes", str(graph["summary"]["node_count"])],
                ["Relationships", str(graph["summary"]["relationship_count"])],
                ["Source files", str(len(graph["metadata"]["source_files"]))],
                ["Graph version", graph["metadata"]["version"]],
                ["Content hash", graph["metadata"]["content_hash"]],
            ],
        ),
        "",
        "## Node Types",
        "",
        markdown_table(["Type", "Count"], node_type_rows),
        "",
        "## Relationship Types",
        "",
        markdown_table(["Type", "Count"], relationship_type_rows),
        "",
        "## Most Connected Nodes",
        "",
        markdown_table(["Node", "Type", "Degree"], connected_rows)
        if connected_rows
        else "No connected nodes yet.",
        "",
        "## Isolated Nodes",
        "",
        markdown_table(["Node", "Type", "ID"], isolated_rows)
        if isolated_rows
        else "No isolated nodes.",
        "",
        "## Source Files",
        "",
    ]

    lines.extend(f"- `{source_file}`" for source_file in graph["metadata"]["source_files"])
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    graph = load_graph()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(build_report(graph), encoding="utf-8")
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
