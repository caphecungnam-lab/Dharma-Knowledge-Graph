#!/usr/bin/env python3
"""Convert a manually captured transcript JSON file into Evidence seed data."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

SOURCE_ID = "source_youtube_fisp_arohzy8"
DOCUMENT_ID = "document_transcript_fisp_arohzy8"
CITATION_ID = "citation_youtube_fisp_arohzy8"

DEFAULT_CONFIDENCE = "low"
DEFAULT_EVIDENCE_TYPE = "transcript_excerpt"
DEFAULT_SOURCE_KIND = "youtube"

REQUIRED_TOP_LEVEL_FIELDS = {
    "source_url",
    "video_id",
    "title",
    "speaker",
    "language",
    "segments",
}

REQUIRED_SEGMENT_FIELDS = {
    "start_time",
    "end_time",
    "text",
    "review_status",
}


class ManualTranscriptError(ValueError):
    """Raised when a manual transcript file cannot be converted safely."""


def is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and value.strip() != ""


def read_json_file(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ManualTranscriptError(f"{path}: invalid JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise ManualTranscriptError(f"{path}: transcript file must be a JSON object")

    return data


def validate_required_top_level_fields(data: dict[str, Any]) -> None:
    for field in sorted(REQUIRED_TOP_LEVEL_FIELDS):
        if field not in data:
            raise ManualTranscriptError(f"missing top-level field: {field}")

    for field in ("source_url", "video_id", "title", "speaker", "language"):
        if not is_non_empty_string(data.get(field)):
            raise ManualTranscriptError(f"empty top-level field: {field}")

    if not isinstance(data.get("segments"), list):
        raise ManualTranscriptError("top-level field 'segments' must be a list")


def validate_required_segment_fields(index: int, segment: dict[str, Any]) -> None:
    for field in sorted(REQUIRED_SEGMENT_FIELDS):
        if field not in segment:
            raise ManualTranscriptError(f"segment {index}: missing {field}")

    for field in ("start_time", "end_time", "review_status"):
        if not is_non_empty_string(segment.get(field)):
            raise ManualTranscriptError(f"segment {index}: empty {field}")

    if not is_non_empty_string(segment.get("text")):
        raise ManualTranscriptError(
            f"segment {index}: empty text cannot be converted to Evidence"
        )


def validate_segment(index: int, segment: object) -> None:
    if not isinstance(segment, dict):
        raise ManualTranscriptError(f"segment {index}: must be an object")

    validate_required_segment_fields(index, segment)


def validate_transcript_data(data: dict[str, Any]) -> None:
    validate_required_top_level_fields(data)

    for index, segment in enumerate(data["segments"]):
        validate_segment(index, segment)


def evidence_id_prefix(video_id: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", video_id.lower()).strip("_")

    if len(normalized) > 4 and "_" not in normalized:
        return f"{normalized[:4]}_{normalized[4:]}"

    return normalized


def evidence_id(video_id: str, index: int) -> str:
    return f"evidence_{evidence_id_prefix(video_id)}_{index + 1:04d}"


def evidence_name(video_id: str, index: int) -> str:
    return f"Transcript excerpt {index + 1:04d} from {video_id}"


def build_evidence_node(
    data: dict[str, Any],
    segment: dict[str, Any],
    index: int,
) -> dict[str, str]:
    video_id = str(data["video_id"]).strip()

    return {
        "id": evidence_id(video_id, index),
        "type": "Evidence",
        "name": evidence_name(video_id, index),
        "evidence_text": str(segment["text"]).strip(),
        "evidence_type": DEFAULT_EVIDENCE_TYPE,
        "language": str(data["language"]).strip(),
        "confidence": DEFAULT_CONFIDENCE,
        "source_kind": DEFAULT_SOURCE_KIND,
        "source_url": str(data["source_url"]).strip(),
        "document_id": DOCUMENT_ID,
        "start_time": str(segment["start_time"]).strip(),
        "end_time": str(segment["end_time"]).strip(),
        "speaker": str(data["speaker"]).strip(),
        "review_status": str(segment["review_status"]).strip(),
        "notes": str(segment.get("notes", "")).strip(),
    }


def build_evidence_relationships(evidence_node_id: str) -> list[dict[str, str]]:
    return [
        {
            "source": DOCUMENT_ID,
            "type": "HAS_EVIDENCE",
            "target": evidence_node_id,
        },
        {
            "source": evidence_node_id,
            "type": "DERIVED_FROM",
            "target": DOCUMENT_ID,
        },
        {
            "source": evidence_node_id,
            "type": "DERIVED_FROM",
            "target": SOURCE_ID,
        },
        {
            "source": evidence_node_id,
            "type": "HAS_CITATION",
            "target": CITATION_ID,
        },
    ]


def convert_transcript_data(data: dict[str, Any]) -> dict[str, list[dict[str, str]]]:
    validate_transcript_data(data)

    nodes: list[dict[str, str]] = []
    relationships: list[dict[str, str]] = []

    for index, segment in enumerate(data["segments"]):
        node = build_evidence_node(data, segment, index)
        nodes.append(node)
        relationships.extend(build_evidence_relationships(node["id"]))

    return {
        "nodes": nodes,
        "relationships": relationships,
    }


def import_transcript_file(input_path: Path) -> dict[str, list[dict[str, str]]]:
    data = read_json_file(input_path)
    return convert_transcript_data(data)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert manual transcript JSON into Evidence seed JSON."
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Manual transcript JSON file",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Optional output JSON path. Defaults to stdout.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        converted = import_transcript_file(args.input)
    except ManualTranscriptError as exc:
        print(f"Transcript import failed: {exc}")
        return 1

    output = json.dumps(converted, indent=2, ensure_ascii=False) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
