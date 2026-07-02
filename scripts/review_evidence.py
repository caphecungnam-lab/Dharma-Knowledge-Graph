#!/usr/bin/env python3
"""Create a human review queue from imported Evidence nodes."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

VIDEO_ID = "FISpARohzy8"
DEFAULT_INPUT_PATH = (
    Path("data") / "processed" / "giac_khang" / VIDEO_ID / "evidence_first_pass.json"
)
DEFAULT_OUTPUT_PATH = (
    Path("data") / "reviewed" / "giac_khang" / VIDEO_ID / "evidence_review_queue.json"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def build_review_node(node: dict[str, Any]) -> dict[str, Any]:
    review_node = deepcopy(node)
    evidence_text = str(node.get("evidence_text", ""))

    review_node["original_evidence_text"] = evidence_text
    review_node["reviewed_evidence_text"] = evidence_text
    review_node["reviewer"] = ""
    review_node["reviewed_at"] = ""
    review_node["review_notes"] = ""
    review_node["review_status"] = "unreviewed"

    return review_node


def build_review_queue(
    source_payload: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    nodes = source_payload.get("nodes", [])
    evidence_nodes = [
        build_review_node(node)
        for node in nodes
        if isinstance(node, dict) and node.get("type") == "Evidence"
    ]

    return {"nodes": evidence_nodes}


def create_review_queue(
    input_path: Path = DEFAULT_INPUT_PATH,
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> dict[str, list[dict[str, Any]]]:
    source_payload = load_json(input_path)
    review_queue = build_review_queue(source_payload)
    write_json(output_path, review_queue)
    return review_queue


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a human review queue from imported Evidence nodes."
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="Input Evidence JSON file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Output review queue JSON file.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    review_queue = create_review_queue(args.input, args.output)
    print(f"Wrote {args.output} with {len(review_queue['nodes'])} Evidence node(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
