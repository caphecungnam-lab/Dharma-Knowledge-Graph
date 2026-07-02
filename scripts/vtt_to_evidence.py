#!/usr/bin/env python3
"""Convert the first real VTT caption segments into Evidence JSON."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

VIDEO_ID = "FISpARohzy8"
SOURCE_URL = "https://www.youtube.com/watch?v=FISpARohzy8"
DOCUMENT_ID = "document_transcript_fisp_arohzy8"
CITATION_ID = "citation_youtube_fisp_arohzy8"
SPEAKER = "HT. Thích Giác Khang"
OUTPUT_PATH = (
    Path("data") / "processed" / "giac_khang" / VIDEO_ID / "evidence_first_pass.json"
)
MAX_EVIDENCE_COUNT = 5
TARGET_DURATION_SECONDS = 20
MIN_DURATION_SECONDS = 5
PREFERRED_MIN_DURATION_SECONDS = 10
MAX_DURATION_SECONDS = 30

TIMESTAMP_LINE = re.compile(
    r"^(?P<start>\d{2}:\d{2}:\d{2}\.\d{3})\s+-->\s+"
    r"(?P<end>\d{2}:\d{2}:\d{2}\.\d{3})"
)
HTML_TAG = re.compile(r"<[^>]+>")
WHITESPACE = re.compile(r"\s+")
SENTENCE_PUNCTUATION = tuple(".?!:;…。！？")


def parse_vtt_timestamp(value: str) -> float:
    parts = value.strip().split(":")
    if len(parts) != 3:
        raise ValueError(f"Invalid VTT timestamp: {value}")

    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])
    return (hours * 3600) + (minutes * 60) + seconds


def format_timestamp(seconds: float) -> str:
    milliseconds = int(round(seconds * 1000))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    whole_seconds, milliseconds = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{whole_seconds:02d}.{milliseconds:03d}"


def clean_caption_text(value: str) -> str:
    without_tags = HTML_TAG.sub("", value)
    unescaped = html.unescape(without_tags)
    return WHITESPACE.sub(" ", unescaped).strip()


def dedupe_adjacent_text(previous: str, current: str) -> str:
    previous = clean_caption_text(previous)
    current = clean_caption_text(current)

    if not current:
        return ""
    if not previous:
        return current
    if current == previous or current in previous:
        return ""
    if current.startswith(previous):
        return current[len(previous) :].strip()

    previous_words = previous.split()
    current_words = current.split()
    max_overlap = min(len(previous_words), len(current_words))

    for overlap_size in range(max_overlap, 0, -1):
        previous_tail = previous_words[-overlap_size:]
        current_head = current_words[:overlap_size]
        if previous_tail == current_head:
            return " ".join(current_words[overlap_size:]).strip()

    return current


def parse_timestamp_line(line: str) -> tuple[str, str] | None:
    match = TIMESTAMP_LINE.match(line.strip())
    if not match:
        return None
    return match.group("start"), match.group("end")


def should_ignore_metadata_line(line: str) -> bool:
    stripped = line.strip()
    return (
        stripped == "WEBVTT"
        or stripped.startswith("Kind:")
        or stripped.startswith("Language:")
        or stripped.startswith("NOTE")
        or stripped.startswith("STYLE")
        or stripped.startswith("REGION")
    )


def parse_vtt_segments(vtt_text: str) -> list[dict[str, str]]:
    segments: list[dict[str, str]] = []
    current_start: str | None = None
    current_end: str | None = None
    text_lines: list[str] = []

    def flush_current_segment() -> None:
        nonlocal current_start, current_end, text_lines

        if current_start and current_end:
            text = clean_caption_text(" ".join(text_lines))
            if text:
                segments.append(
                    {
                        "start_time": current_start,
                        "end_time": current_end,
                        "text": text,
                    }
                )

        current_start = None
        current_end = None
        text_lines = []

    for line in vtt_text.splitlines():
        timestamp = parse_timestamp_line(line)
        if timestamp:
            flush_current_segment()
            current_start, current_end = timestamp
            continue

        if not line.strip():
            if current_start is not None and not text_lines:
                continue
            flush_current_segment()
            continue

        if current_start is None and should_ignore_metadata_line(line):
            continue

        if current_start is not None:
            text_lines.append(line)

    flush_current_segment()
    return segments


def segment_duration(segment: dict[str, str]) -> float:
    return parse_vtt_timestamp(segment["end_time"]) - parse_vtt_timestamp(
        segment["start_time"]
    )


def should_close_segment(segment: dict[str, str]) -> bool:
    duration = segment_duration(segment)
    text = segment["text"].strip()

    if duration >= MAX_DURATION_SECONDS:
        return True
    if duration < PREFERRED_MIN_DURATION_SECONDS:
        return False
    if duration >= TARGET_DURATION_SECONDS:
        return True
    return text.endswith(SENTENCE_PUNCTUATION)


def merge_cues(cues: list[dict]) -> list[dict]:
    merged: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    last_merged_text = ""

    for cue in cues:
        cue_text = clean_caption_text(cue.get("text", ""))
        if not cue_text:
            continue

        if current is None:
            cue_text = dedupe_adjacent_text(last_merged_text, cue_text)
            if not cue_text:
                continue

            current = {
                "start_time": cue["start_time"],
                "end_time": cue["end_time"],
                "text": cue_text,
            }
        else:
            new_text = dedupe_adjacent_text(current["text"], cue_text)
            current["end_time"] = cue["end_time"]
            if new_text:
                current["text"] = clean_caption_text(f"{current['text']} {new_text}")

        if current and should_close_segment(current):
            merged.append(current)
            last_merged_text = current["text"]
            current = None

    if current and segment_duration(current) >= MIN_DURATION_SECONDS:
        merged.append(current)

    return merged


def evidence_id(index: int) -> str:
    return f"evidence_fisp_arohzy8_{index + 1:04d}"


def build_evidence_node(segment: dict[str, str], index: int) -> dict[str, str]:
    return {
        "id": evidence_id(index),
        "type": "Evidence",
        "name": f"VTT caption excerpt {index + 1:04d} from {VIDEO_ID}",
        "evidence_text": segment["text"],
        "evidence_type": "transcript_excerpt",
        "language": "vi",
        "confidence": "low",
        "source_kind": "youtube",
        "source_url": SOURCE_URL,
        "document_id": DOCUMENT_ID,
        "start_time": segment["start_time"],
        "end_time": segment["end_time"],
        "speaker": SPEAKER,
        "review_status": "unreviewed",
        "notes": (
            "Imported from YouTube VTT caption. Needs human review for "
            "Buddhist terminology."
        ),
    }


def build_evidence_relationships(evidence_node_id: str) -> list[dict[str, str]]:
    return [
        {
            "source": evidence_node_id,
            "type": "HAS_CITATION",
            "target": CITATION_ID,
        },
        {
            "source": evidence_node_id,
            "type": "DERIVED_FROM",
            "target": DOCUMENT_ID,
        },
    ]


def convert_vtt_to_evidence(
    vtt_text: str,
    max_evidence_count: int = MAX_EVIDENCE_COUNT,
) -> dict[str, list[dict[str, str]]]:
    segments = merge_cues(parse_vtt_segments(vtt_text))[:max_evidence_count]
    nodes: list[dict[str, str]] = []
    relationships: list[dict[str, str]] = []

    for index, segment in enumerate(segments):
        node = build_evidence_node(segment, index)
        nodes.append(node)
        relationships.extend(build_evidence_relationships(node["id"]))

    return {
        "nodes": nodes,
        "relationships": relationships,
    }


def convert_vtt_file(input_path: Path, output_path: Path = OUTPUT_PATH) -> dict:
    vtt_text = input_path.read_text(encoding="utf-8")
    output = convert_vtt_to_evidence(vtt_text)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert first VTT caption segments into Evidence JSON."
    )
    parser.add_argument("input", type=Path, help="Input .vtt file path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = convert_vtt_file(args.input)
    print(f"Wrote {OUTPUT_PATH} with {len(output['nodes'])} Evidence node(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
