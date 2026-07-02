#!/usr/bin/env python3
"""Build processed graph artifacts from seed data."""

from __future__ import annotations

import json
import hashlib
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED_DIR = ROOT / "data" / "seeds"
PROCESSED_DIR = ROOT / "data" / "processed"
EXPLORER_DIR = ROOT / "docs" / "graph-explorer"
DOCS_ARTIFACTS_DIR = ROOT / "docs" / "artifacts"
GIAC_KHANG_VIDEO_DIR = Path("giac_khang") / "FISpARohzy8"
GIAC_KHANG_SEED_FILES = [
    ROOT / "data" / "seeds" / "giac_khang_kinh_sau_sau_fisp_arohzy8.json",
]
GIAC_KHANG_OPTIONAL_FILES = [
    PROCESSED_DIR / GIAC_KHANG_VIDEO_DIR / "evidence_first_pass.json",
    ROOT / "data" / "reviewed" / GIAC_KHANG_VIDEO_DIR / "evidence_review_queue.json",
    ROOT / "data" / "curated" / GIAC_KHANG_VIDEO_DIR / "evidence_curated.json",
]


def read_graph_files(paths: list[Path]) -> list[tuple[Path, dict]]:
    return [
        (path, json.loads(path.read_text(encoding="utf-8")))
        for path in paths
        if path.exists()
    ]


def read_seed_files() -> list[tuple[Path, dict]]:
    return read_graph_files(sorted(SEED_DIR.glob("*.json")))


def read_giac_khang_files() -> list[tuple[Path, dict]]:
    return read_graph_files(GIAC_KHANG_SEED_FILES + GIAC_KHANG_OPTIONAL_FILES)


def read_all_data_files() -> list[tuple[Path, dict]]:
    seed_paths = sorted(SEED_DIR.glob("*.json"))
    return read_graph_files(seed_paths + GIAC_KHANG_OPTIONAL_FILES)


def source_content_hash(graph_files: list[tuple[Path, dict]]) -> str:
    digest = hashlib.sha256()

    for path, data in graph_files:
        digest.update(str(path.relative_to(ROOT)).encode("utf-8"))
        digest.update(b"\0")
        digest.update(
            json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8")
        )
        digest.update(b"\0")

    return digest.hexdigest()


def source_badge_for_path(path: Path, node: dict | None = None) -> str:
    if node and node.get("type") == "Corpus":
        return "corpus"

    if path in GIAC_KHANG_SEED_FILES:
        return "pilot"

    relative_parts = path.relative_to(ROOT).parts
    if len(relative_parts) < 2:
        return "seed"

    source_dir = relative_parts[1]
    if source_dir in {"seeds", "processed", "reviewed", "curated"}:
        return "seed" if source_dir == "seeds" else source_dir

    return "seed"


def summarize_graph(nodes: list[dict], relationships: list[dict]) -> dict:
    node_type_counts = Counter(node["type"] for node in nodes)
    relationship_type_counts = Counter(rel["type"] for rel in relationships)
    source_badge_counts = Counter(node.get("source_badge", "seed") for node in nodes)

    return {
        "node_count": len(nodes),
        "relationship_count": len(relationships),
        "node_type_counts": dict(sorted(node_type_counts.items())),
        "relationship_type_counts": dict(sorted(relationship_type_counts.items())),
        "source_badge_counts": dict(sorted(source_badge_counts.items())),
    }


def build_graph_from_files(
    graph_files: list[tuple[Path, dict]],
    mode: str,
    title: str = "Dharma Knowledge Graph",
) -> dict:
    nodes: dict[str, dict] = {}
    relationships: dict[tuple[str, str, str], dict] = {}
    source_files: list[str] = []

    for path, data in graph_files:
        source_files.append(str(path.relative_to(ROOT)))

        for node in data["nodes"]:
            enriched_node = dict(node)
            enriched_node["source_file"] = str(path.relative_to(ROOT))
            enriched_node["source_badge"] = source_badge_for_path(path, node)
            nodes[enriched_node["id"]] = enriched_node

        for relationship in data.get("relationships", []):
            enriched_relationship = dict(relationship)
            enriched_relationship["source_file"] = str(path.relative_to(ROOT))
            enriched_relationship["source_badge"] = source_badge_for_path(path)
            relationship_key = (
                str(enriched_relationship.get("source", "")),
                str(enriched_relationship.get("type", "")),
                str(enriched_relationship.get("target", "")),
            )
            relationships[relationship_key] = enriched_relationship

    node_list = sorted(nodes.values(), key=lambda node: (node["type"], node["name"]))
    relationship_list = sorted(
        relationships.values(),
        key=lambda rel: (rel["type"], rel["source"], rel["target"]),
    )

    return {
        "metadata": {
            "title": title,
            "version": "0.1",
            "mode": mode,
            "content_hash": source_content_hash(graph_files),
            "source_files": source_files,
        },
        "summary": summarize_graph(node_list, relationship_list),
        "nodes": node_list,
        "relationships": relationship_list,
    }


def build_graph(mode: str = "all_data") -> dict:
    if mode == "giac_khang":
        return build_graph_from_files(
            read_giac_khang_files(),
            mode="giac_khang",
            title="Dharma Knowledge Graph: Giác Khang Corpus",
        )
    if mode == "seeds_only":
        return build_graph_from_files(
            read_seed_files(),
            mode="seeds_only",
            title="Dharma Knowledge Graph: Seeds",
        )
    if mode == "all_data":
        return build_graph_from_files(
            read_all_data_files(),
            mode="all_data",
            title="Dharma Knowledge Graph: All Data",
        )

    raise ValueError(f"Unknown graph mode: {mode}")


def build_explorer_scopes() -> dict:
    return {
        "default_mode": "giac_khang",
        "modes": {
            "giac_khang": build_graph("giac_khang"),
            "seeds_only": build_graph("seeds_only"),
            "all_data": build_graph("all_data"),
        },
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
    default_graph_json = json.dumps(
        data["modes"][data["default_mode"]],
        indent=2,
        ensure_ascii=False,
    )
    path.write_text(
        f"window.DHARMA_GRAPH_SCOPES = {graph_json};\n"
        f"window.DHARMA_GRAPH = {default_graph_json};\n",
        encoding="utf-8",
    )


def main() -> int:
    graph = build_graph("all_data")
    explorer_scopes = build_explorer_scopes()
    graph_json_path = PROCESSED_DIR / "graph.json"
    docs_graph_json_path = DOCS_ARTIFACTS_DIR / "graph.json"
    graph_data_path = EXPLORER_DIR / "graph-data.js"

    write_json(graph_json_path, graph)
    write_json(docs_graph_json_path, graph)
    write_explorer_data(graph_data_path, explorer_scopes)

    print(f"Wrote {graph_json_path.relative_to(ROOT)}")
    print(f"Wrote {docs_graph_json_path.relative_to(ROOT)}")
    print(f"Wrote {graph_data_path.relative_to(ROOT)}")
    print(
        f"Graph has {graph['summary']['node_count']} nodes and "
        f"{graph['summary']['relationship_count']} relationships."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
