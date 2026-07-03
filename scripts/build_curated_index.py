#!/usr/bin/env python3
"""Build a merged curated Evidence index for the Giac Khang corpus."""

from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dharma_kg.citations import build_youtube_timestamp_url  # noqa: E402
from dharma_kg.quality import score_evidence  # noqa: E402

CORPUS_ID = "corpus_giac_khang"
INDEX_NAME = "giac_khang_curated_evidence_index"
DEFAULT_INPUT_DIR = Path("data") / "curated" / "giac_khang"
DEFAULT_OUTPUT_PATH = (
    Path("data") / "indexes" / "giac_khang" / "curated_evidence_index.json"
)
CURATED_FILE_PATTERNS = ("*_curated.json", "evidence_curated.json")


def current_local_iso_datetime() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def find_curated_files(input_dir: Path) -> list[Path]:
    paths: set[Path] = set()

    for pattern in CURATED_FILE_PATTERNS:
        paths.update(input_dir.rglob(pattern))

    return sorted(path for path in paths if path.is_file())


def is_evidence_node(node: Any) -> bool:
    return isinstance(node, dict) and node.get("type") == "Evidence"


def source_file_label(path: Path) -> str:
    return str(path)


def enriched_node(node: dict[str, Any], path: Path) -> dict[str, Any]:
    copy = deepcopy(node)
    copy.setdefault("source_file", source_file_label(path))
    if is_evidence_node(copy):
        citation_url = build_youtube_timestamp_url(
            str(copy.get("source_url", "")),
            str(copy.get("start_time", "")),
        )
        if citation_url:
            copy.setdefault("citation_url", citation_url)
        copy.update(score_evidence(copy))
    return copy


def curated_rank(node: dict[str, Any]) -> tuple[int, str]:
    curated_status_rank = 1 if node.get("curated_status") == "curated" else 0
    return curated_status_rank, str(node.get("curated_at", ""))


def should_replace_evidence(
    existing: dict[str, Any],
    candidate: dict[str, Any],
) -> bool:
    return curated_rank(candidate) >= curated_rank(existing)


def relationship_key(relationship: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(relationship.get("source", "")),
        str(relationship.get("type", "")),
        str(relationship.get("target", "")),
    )


def evidence_sort_key(node: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(node.get("document_id") or node.get("source_id") or ""),
        str(node.get("start_time", "")),
        str(node.get("id", "")),
    )


def node_sort_key(node: dict[str, Any]) -> tuple[int, str, str, str]:
    if node.get("type") == "Evidence":
        document_id, start_time, evidence_id = evidence_sort_key(node)
        return 0, document_id, start_time, evidence_id
    return (
        1,
        str(node.get("type", "")),
        str(node.get("name", "")),
        str(node.get("id", "")),
    )


def build_curated_index_from_files(paths: list[Path]) -> dict[str, Any]:
    evidence_nodes: dict[str, dict[str, Any]] = {}
    context_nodes: dict[str, dict[str, Any]] = {}
    relationships: dict[tuple[str, str, str], dict[str, Any]] = {}
    source_files: list[str] = []

    for path in sorted(paths):
        payload = load_json(path)
        source_files.append(source_file_label(path))

        for node in payload.get("nodes", []):
            if not isinstance(node, dict):
                continue

            node_id = str(node.get("id", ""))
            if not node_id:
                continue

            copy = enriched_node(node, path)
            if is_evidence_node(copy):
                existing = evidence_nodes.get(node_id)
                if existing is None or should_replace_evidence(existing, copy):
                    evidence_nodes[node_id] = copy
            else:
                context_nodes.setdefault(node_id, copy)

        for relationship in payload.get("relationships", []):
            if not isinstance(relationship, dict):
                continue
            relationships[relationship_key(relationship)] = deepcopy(relationship)

    evidence_list = sorted(evidence_nodes.values(), key=evidence_sort_key)
    context_list = sorted(context_nodes.values(), key=node_sort_key)
    relationship_list = sorted(
        relationships.values(),
        key=lambda relationship: (
            str(relationship.get("type", "")),
            str(relationship.get("source", "")),
            str(relationship.get("target", "")),
        ),
    )

    return {
        "metadata": {
            "index_name": INDEX_NAME,
            "corpus_id": CORPUS_ID,
            "generated_at": current_local_iso_datetime(),
            "evidence_count": len(evidence_list),
            "source_files": source_files,
        },
        "nodes": evidence_list + context_list,
        "relationships": relationship_list,
    }


def build_curated_index(input_dir: Path, output_path: Path) -> dict[str, Any]:
    paths = find_curated_files(input_dir)
    index = build_curated_index_from_files(paths)
    write_json(output_path, index)
    return index


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a merged curated Evidence index."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help="Directory containing curated Evidence JSON files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Output curated Evidence index JSON path.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    index = build_curated_index(args.input_dir, args.output)
    print(
        f"Wrote {args.output} with {index['metadata']['evidence_count']} Evidence node(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
