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
DEFAULT_SPEAKER = "HT. Thích Giác Khang"
DEFAULT_LANGUAGE = "vi"
DEFAULT_SOURCE_KIND = "youtube"
DEFAULT_CONFIDENCE = "low"
DEFAULT_EVIDENCE_TYPE = "transcript_excerpt"

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


def read_manual_transcript(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ManualTranscriptError(f"{path}: invalid JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise ManualTranscriptError(f"{path}: transcript file must be a JSON object")

    segments = data.get("segments")
    if not isinstance(segments, list):
        raise ManualTranscriptError(f"{path}: 'segments' must be a list")

    return data


def evidence_id_prefix(video_id: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", video_id.lower()).strip("_")
    if len(normalized) > 4 and "_" not in normalized:
        return f"{normalized[:4]}_{normalized[4:]}"
    return normalized


def effective_source_url(data: dict[str, Any], segment: dict[str, Any]) -> object:
    return segment.get("source_url", data.get("source_url"))


def validate_segment(
    data: dict[str, Any],
    index: int,
    segment: object,
    *,
    require_text: bool,
) -> None:
    if not isinstance(segment, dict):
        raise ManualTranscriptError(f"segment {index}: must be an object")

    source_url = effective_source_url(data, segment)
    if not is_non_empty_string(source_url):
        raise ManualTranscriptError(f"segment {index}: missing source_url")

    for field in sorted(REQUIRED_SEGMENT_FIELDS):
        if field not in segment:
            raise ManualTranscriptError(f"segment {index}: missing {field}")

    for field in ("start_time", "end_time", "review_status"):
        if not is_non_empty_string(segment.get(field)):
            raise ManualTranscriptError(f"segment {index}: empty {field}")

    text = segment.get("text")
    if require_text and not is_non_empty_string(text):
        raise ManualTranscriptError(
            f"segment {index}: empty text cannot be converted to Evidence"
        )


def validate_manual_transcript(data: dict[str, Any], *, require_text: bool) -> None:
    segments = data.get("segments")
    if not isinstance(segments, list):
        raise ManualTranscriptError("'segments' must be a list")

    for index, segment in enumerate(segments):
        validate_segment(data, index, segment, require_text=require_text)


def segment_locator(segment: dict[str, Any]) -> str:
    if is_non_empty_string(segment.get("locator")):
        return str(segment["locator"]).strip()
    return f"{segment['start_time']}-{segment['end_time']}"


def evidence_node(
    data: dict[str, Any],
    segment: dict[str, Any],
    index: int,
) -> dict[str, str]:
    video_id = str(data.get("video_id", "FISpARohzy8"))
    evidence_id = f"evidence_{evidence_id_prefix(video_id)}_{index + 1:04d}"
    source_url = str(effective_source_url(data, segment)).strip()
    speaker = str(data.get("speaker") or DEFAULT_SPEAKER).strip()

    return {
        "id": evidence_id,
        "type": "Evidence",
        "name": f"Transcript excerpt {index + 1:04d} from {video_id}",
        "evidence_text": str(segment["text"]).strip(),
        "evidence_type": DEFAULT_EVIDENCE_TYPE,
        "language": str(data.get("language") or DEFAULT_LANGUAGE),
        "confidence": DEFAULT_CONFIDENCE,
        "source_kind": DEFAULT_SOURCE_KIND,
        "source_url": source_url,
        "document_id": DOCUMENT_ID,
        "locator": segment_locator(segment),
        "start_time": str(segment["start_time"]),
        "end_time": str(segment["end_time"]),
        "speaker": speaker,
        "review_status": str(segment["review_status"]),
        "notes": str(segment.get("notes", "")),
    }


def evidence_relationships(evidence_id: str) -> list[dict[str, str]]:
    return [
        {
            "source": DOCUMENT_ID,
            "type": "HAS_EVIDENCE",
            "target": evidence_id,
        },
        {
            "source": evidence_id,
            "type": "DERIVED_FROM",
            "target": DOCUMENT_ID,
        },
        {
            "source": evidence_id,
            "type": "DERIVED_FROM",
            "target": SOURCE_ID,
        },
        {
            "source": evidence_id,
            "type": "HAS_CITATION",
            "target": CITATION_ID,
        },
    ]


def convert_manual_transcript(data: dict[str, Any]) -> dict[str, list[dict[str, str]]]:
    validate_manual_transcript(data, require_text=True)

    nodes: list[dict[str, str]] = []
    relationships: list[dict[str, str]] = []
    for index, segment in enumerate(data["segments"]):
        node = evidence_node(data, segment, index)
        nodes.append(node)
        relationships.extend(evidence_relationships(node["id"]))

    return {
        "nodes": nodes,
        "relationships": relationships,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert manual transcript JSON into Evidence seed JSON."
    )
    parser.add_argument("input", type=Path, help="Manual transcript JSON file")
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
        data = read_manual_transcript(args.input)
        converted = convert_manual_transcript(data)
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
