#!/usr/bin/env python3
"""Write a Markdown quality report for the processed Dharma graph."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = ROOT / "data" / "processed" / "graph.json"
REPORT_PATH = ROOT / "docs" / "reports" / "quality-report.md"


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
    incoming = defaultdict(list)
    outgoing = defaultdict(list)

    for relationship in relationships:
        degree[relationship["source"]] += 1
        degree[relationship["target"]] += 1
        outgoing[relationship["source"]].append(relationship)
        incoming[relationship["target"]].append(relationship)

    concepts = [node for node in nodes if node["type"] == "Concept"]
    terms = [node for node in nodes if node["type"] == "Term"]
    texts = [node for node in nodes if node["type"] == "Text"]
    citations = [node for node in nodes if node["type"] == "Citation"]

    concepts_with_terms = {
        relationship["target"]
        for relationship in relationships
        if relationship["type"] == "DEFINES"
        and node_by_id[relationship["source"]]["type"] == "Term"
        and node_by_id[relationship["target"]]["type"] == "Concept"
    }
    concepts_without_terms = [
        node for node in concepts if node["id"] not in concepts_with_terms
    ]
    texts_without_citations = [
        node
        for node in texts
        if not any(rel["type"] == "CITES" for rel in outgoing[node["id"]])
    ]
    citations_without_concepts = [
        node
        for node in citations
        if not any(rel["type"] == "MENTIONS" for rel in outgoing[node["id"]])
    ]
    isolated_nodes = [node for node in nodes if degree[node["id"]] == 0]

    coverage_rows = [
        ["Nodes", str(len(nodes))],
        ["Relationships", str(len(relationships))],
        ["Concepts", str(len(concepts))],
        ["Terms", str(len(terms))],
        ["Concepts with term definitions", str(len(concepts_with_terms))],
        ["Concepts without term definitions", str(len(concepts_without_terms))],
        ["Texts", str(len(texts))],
        ["Texts without citations", str(len(texts_without_citations))],
        ["Citations", str(len(citations))],
        ["Citations without concept mentions", str(len(citations_without_concepts))],
        ["Isolated nodes", str(len(isolated_nodes))],
    ]

    concept_gap_rows = [
        [node["name"], node["id"], node.get("category", "")]
        for node in sorted(concepts_without_terms, key=lambda item: item["name"])
    ]
    text_gap_rows = [
        [node["name"], node["id"]]
        for node in sorted(texts_without_citations, key=lambda item: item["name"])
    ]
    citation_gap_rows = [
        [node["name"], node["id"]]
        for node in sorted(citations_without_concepts, key=lambda item: item["name"])
    ]
    isolated_rows = [
        [node["name"], node["type"], node["id"]]
        for node in sorted(isolated_nodes, key=lambda item: item["name"])
    ]

    lines = [
        "# Graph Quality Report",
        "",
        "Generated from `data/processed/graph.json`.",
        "",
        "## Coverage",
        "",
        markdown_table(["Metric", "Value"], coverage_rows),
        "",
        "## Concepts Without Term Definitions",
        "",
        markdown_table(["Concept", "ID", "Category"], concept_gap_rows)
        if concept_gap_rows
        else "Every concept has at least one term definition.",
        "",
        "## Texts Without Citations",
        "",
        markdown_table(["Text", "ID"], text_gap_rows)
        if text_gap_rows
        else "Every text has at least one citation.",
        "",
        "## Citations Without Concept Mentions",
        "",
        markdown_table(["Citation", "ID"], citation_gap_rows)
        if citation_gap_rows
        else "Every citation mentions at least one concept.",
        "",
        "## Isolated Nodes",
        "",
        markdown_table(["Node", "Type", "ID"], isolated_rows)
        if isolated_rows
        else "No isolated nodes.",
        "",
    ]

    return "\n".join(lines)


def main() -> int:
    graph = load_graph()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(build_report(graph), encoding="utf-8")
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
