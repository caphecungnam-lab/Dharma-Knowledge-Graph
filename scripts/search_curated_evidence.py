#!/usr/bin/env python3
"""Search curated Evidence with citation context."""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dharma_kg.citations import (  # noqa: E402
    build_youtube_timestamp_url,
    extract_youtube_video_id,
)

DEFAULT_INPUT_PATH = (
    Path("data") / "indexes" / "giac_khang" / "curated_evidence_index.json"
)
SEARCH_FIELDS = (
    "evidence_text",
    "reviewed_evidence_text",
    "original_evidence_text",
    "notes",
    "review_notes",
    "name",
)
QUERY_ALIASES = {
    "kinh sau sau": (
        "kinh 66",
        "kinh sáu sáu",
        "bài kinh 66",
    ),
    "sau sau": (
        "66",
        "sáu sáu",
    ),
    "luc can": (
        "lục căn",
        "sáu căn",
    ),
    "luc tran": (
        "lục trần",
        "sáu trần",
    ),
    "luc thuc": (
        "lục thức",
        "sáu thức",
    ),
}
WHITESPACE = re.compile(r"\s+")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def strip_vietnamese_diacritics(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value)
    without_marks = "".join(
        character for character in normalized if unicodedata.category(character) != "Mn"
    )
    return without_marks.replace("đ", "d").replace("Đ", "D")


def normalize_text(value: str, remove_diacritics: bool = True) -> str:
    normalized = WHITESPACE.sub(" ", value.casefold().strip())
    if remove_diacritics:
        normalized = strip_vietnamese_diacritics(normalized)
    return normalized


def normalize_query_terms(query: str) -> list[str]:
    terms: list[str] = []
    candidate_terms = [query]
    normalized_query = normalize_text(query)
    candidate_terms.extend(QUERY_ALIASES.get(normalized_query, ()))

    for term in candidate_terms:
        for normalized_term in {normalize_text(term), normalize_text(term, False)}:
            if normalized_term and normalized_term not in terms:
                terms.append(normalized_term)

    return terms


def searchable_text(node: dict[str, Any]) -> str:
    return "\n".join(str(node.get(field, "")) for field in SEARCH_FIELDS)


def build_citation_string(node: dict[str, Any]) -> str:
    source_url = str(node.get("source_url", ""))
    start_time = str(node.get("start_time", ""))
    end_time = str(node.get("end_time", ""))
    speaker = str(node.get("speaker", ""))
    source_identity = str(
        node.get("video_id")
        or node.get("source_id")
        or extract_youtube_video_id(source_url)
        or ""
    )

    time_range = " -> ".join(value for value in [start_time, end_time] if value)
    parts = [
        part for part in [source_identity, speaker, time_range, source_url] if part
    ]
    return " | ".join(parts)


def evidence_result(node: dict[str, Any]) -> dict[str, Any]:
    source_url = str(node.get("source_url", ""))
    start_time = str(node.get("start_time", ""))
    return {
        "id": node.get("id", ""),
        "start_time": start_time,
        "end_time": node.get("end_time", ""),
        "speaker": node.get("speaker", ""),
        "review_status": node.get("review_status", ""),
        "curated_status": node.get("curated_status", ""),
        "evidence_text": node.get("evidence_text", ""),
        "source_url": source_url,
        "source_id": node.get("source_id", ""),
        "video_id": node.get("video_id", "")
        or extract_youtube_video_id(source_url)
        or "",
        "citation_url": node.get("citation_url")
        or build_youtube_timestamp_url(source_url, start_time),
        "citation": build_citation_string(node),
    }


def search_curated_evidence(
    payload: dict[str, Any],
    query: str,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    query_terms = normalize_query_terms(query)
    matches: list[dict[str, Any]] = []

    for node in payload.get("nodes", []):
        if not isinstance(node, dict) or node.get("type") != "Evidence":
            continue

        node_text = searchable_text(node)
        searchable_versions = {
            normalize_text(node_text),
            normalize_text(node_text, remove_diacritics=False),
        }

        if any(
            query_term in searchable_version
            for query_term in query_terms
            for searchable_version in searchable_versions
        ):
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


def build_debug_info(
    path: Path,
    payload: dict[str, Any],
    query: str,
) -> dict[str, Any]:
    evidence_nodes = [
        node
        for node in payload.get("nodes", [])
        if isinstance(node, dict) and node.get("type") == "Evidence"
    ]
    return {
        "path": str(path),
        "curated_file_path": str(path),
        "evidence_node_count": len(evidence_nodes),
        "query_terms": normalize_query_terms(query),
        "normalized_query_terms": normalize_query_terms(query),
        "searched_fields": list(SEARCH_FIELDS),
        "fields_searched": list(SEARCH_FIELDS),
    }


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
    if result.get("citation_url"):
        lines.append(f"Citation URL: {result['citation_url']}")
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
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print search normalization details before results.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = load_json(args.path)
    results = search_curated_evidence(payload, args.query, limit=args.limit)
    debug_info = build_debug_info(args.path, payload, args.query)

    if args.json:
        output: Any = (
            {"debug": debug_info, "results": results} if args.debug else results
        )
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        if args.debug:
            print(f"path: {debug_info['path']}")
            print(f"curated_file_path: {debug_info['curated_file_path']}")
            print(f"evidence_node_count: {debug_info['evidence_node_count']}")
            print(
                "normalized_query_terms: "
                + ", ".join(debug_info["normalized_query_terms"])
            )
            print("fields_searched: " + ", ".join(debug_info["fields_searched"]))
            print()
        print(format_text_results(results))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
