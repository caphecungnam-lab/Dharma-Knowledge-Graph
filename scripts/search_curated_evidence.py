#!/usr/bin/env python3
"""Search curated Evidence with citation context."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DEFAULT_INPUT_PATH = (
    Path("data") / "curated" / "giac_khang" / "FISpARohzy8" / "evidence_curated.json"
)
SEARCH_FIELDS = (
    "evidence_text",
    "reviewed_evidence_text",
    "original_evidence_text",
    "notes",
    "review_notes",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def searchable_text(node: dict[str, Any]) -> str:
    return "\n".join(str(node.get(field, "")) for field in SEARCH_FIELDS)


def build_citation_string(node: dict[str, Any]) -> str:
    source_url = str(node.get("source_url", ""))
    start_time = str(node.get("start_time", ""))
    end_time = str(node.get("end_time", ""))
    speaker = str(node.get("speaker", ""))

    time_range = " -> ".join(value for value in [start_time, end_time] if value)
    parts = [part for part in [speaker, time_range, source_url] if part]
    return " | ".join(parts)


def evidence_result(node: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": node.get("id", ""),
        "start_time": node.get("start_time", ""),
        "end_time": node.get("end_time", ""),
        "speaker": node.get("speaker", ""),
        "review_status": node.get("review_status", ""),
        "curated_status": node.get("curated_status", ""),
        "evidence_text": node.get("evidence_text", ""),
        "source_url": node.get("source_url", ""),
        "citation": build_citation_string(node),
    }


def search_curated_evidence(
    payload: dict[str, Any],
    query: str,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    normalized_query = query.casefold()
    matches: list[dict[str, Any]] = []

    for node in payload.get("nodes", []):
        if not isinstance(node, dict) or node.get("type") != "Evidence":
            continue

        if normalized_query in searchable_text(node).casefold():
            matches.append(evidence_result(node))

        if limit is not None and len(matches) >= limit:
            break

    return matches


def search_curated_evidence_file(
    query: str,
    path: Path = DEFAULT_INPUT_PATH,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    return search_curated_evidence(load_json(path), query, limit=limit)


def format_text_result(result: dict[str, Any]) -> str:
    lines = [
        f"id: {result['id']}",
        f"start_time: {result['start_time']}",
        f"end_time: {result['end_time']}",
        f"speaker: {result['speaker']}",
        f"review_status: {result['review_status']}",
        f"curated_status: {result['curated_status']}",
        f"evidence_text: {result['evidence_text']}",
        f"source_url: {result['source_url']}",
        f"citation: {result['citation']}",
    ]
    return "\n".join(lines)


def format_text_results(results: list[dict[str, Any]]) -> str:
    if not results:
        return "No matching curated Evidence found."

    return "\n\n".join(format_text_result(result) for result in results)


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("--limit must be a positive integer")
    return parsed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search curated Evidence and print citation-aware results."
    )
    parser.add_argument("query", help="Search query.")
    parser.add_argument(
        "--limit",
        type=positive_int,
        default=None,
        help="Maximum number of results to print.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print results as JSON.",
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="Path to curated Evidence JSON.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    results = search_curated_evidence_file(args.query, path=args.path, limit=args.limit)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(format_text_results(results))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
