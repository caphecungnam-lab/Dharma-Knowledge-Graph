#!/usr/bin/env python3
"""CLI helper for reviewing batch Evidence JSON safely."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

VIDEO_ID = "FISpARohzy8"
DEFAULT_INPUT_PATH = (
    Path("data") / "processed" / "giac_khang" / VIDEO_ID / "evidence_batch_001.json"
)
DEFAULT_REVIEW_PATH = (
    Path("data")
    / "reviewed"
    / "giac_khang"
    / VIDEO_ID
    / "evidence_batch_001_review_queue.json"
)
APPROVED_WITHOUT_CHANGES = "Approved without text changes."


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def is_evidence_node(node: Any) -> bool:
    return isinstance(node, dict) and node.get("type") == "Evidence"


def short_text(value: str, limit: int = 72) -> str:
    cleaned = " ".join(str(value).split())
    if len(cleaned) <= limit:
        return cleaned
    return f"{cleaned[: limit - 1]}..."


def build_review_node(node: dict[str, Any]) -> dict[str, Any]:
    review_node = deepcopy(node)
    evidence_text = str(node.get("evidence_text", ""))
    original_review_status = str(node.get("review_status", ""))

    review_node.pop("review_status", None)
    review_node["original_review_status"] = original_review_status
    review_node["original_evidence_text"] = evidence_text
    review_node["reviewed_evidence_text"] = evidence_text
    review_node["reviewer"] = None
    review_node["reviewed_at"] = None
    review_node["review_notes"] = None
    review_node["review_status"] = "unreviewed"

    return review_node


def init_review_queue_payload(source_payload: dict[str, Any]) -> dict[str, Any]:
    nodes = [
        build_review_node(node) if is_evidence_node(node) else deepcopy(node)
        for node in source_payload.get("nodes", [])
    ]
    relationships = deepcopy(source_payload.get("relationships", []))

    return {
        "nodes": nodes,
        "relationships": relationships,
    }


def init_review_queue(input_path: Path, output_path: Path) -> dict[str, Any]:
    source_payload = load_json(input_path)
    review_queue = init_review_queue_payload(source_payload)
    write_json(output_path, review_queue)
    return review_queue


def evidence_nodes(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [node for node in payload.get("nodes", []) if is_evidence_node(node)]


def find_evidence(payload: dict[str, Any], evidence_id: str) -> dict[str, Any]:
    for node in evidence_nodes(payload):
        if node.get("id") == evidence_id:
            return node
    raise ValueError(f"Evidence not found: {evidence_id}")


def format_list(payload: dict[str, Any]) -> str:
    lines = [
        "evidence_id | start_time | end_time | review_status | reviewed_evidence_text"
    ]
    for node in evidence_nodes(payload):
        lines.append(
            " | ".join(
                [
                    str(node.get("id", "")),
                    str(node.get("start_time", "")),
                    str(node.get("end_time", "")),
                    str(node.get("review_status", "")),
                    short_text(str(node.get("reviewed_evidence_text", ""))),
                ]
            )
        )
    return "\n".join(lines)


def format_show(node: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"id: {node.get('id', '')}",
            f"time: {node.get('start_time', '')} -> {node.get('end_time', '')}",
            f"speaker: {node.get('speaker', '')}",
            f"original_evidence_text: {node.get('original_evidence_text', '')}",
            f"reviewed_evidence_text: {node.get('reviewed_evidence_text', '')}",
            f"review_status: {node.get('review_status', '')}",
            f"reviewer: {node.get('reviewer')}",
            f"reviewed_at: {node.get('reviewed_at')}",
            f"review_notes: {node.get('review_notes')}",
            f"source_url: {node.get('source_url', '')}",
        ]
    )


def list_review_queue(path: Path) -> str:
    return format_list(load_json(path))


def show_evidence(path: Path, evidence_id: str) -> str:
    payload = load_json(path)
    return format_show(find_evidence(payload, evidence_id))


def update_review_node(
    path: Path,
    evidence_id: str,
    review_status: str,
    reviewer: str,
    reviewed_text: str | None = None,
    notes: str | None = None,
    reviewed_at: str | None = None,
) -> dict[str, Any]:
    payload = load_json(path)
    node = find_evidence(payload, evidence_id)

    if reviewed_text is not None:
        node["reviewed_evidence_text"] = reviewed_text

    node["review_status"] = review_status
    node["reviewer"] = reviewer
    node["reviewed_at"] = reviewed_at or now_iso()
    node["review_notes"] = notes

    write_json(path, payload)
    return node


def approve_evidence(
    path: Path,
    evidence_id: str,
    reviewer: str,
    notes: str | None = None,
    reviewed_at: str | None = None,
) -> dict[str, Any]:
    return update_review_node(
        path,
        evidence_id,
        review_status="human_reviewed",
        reviewer=reviewer,
        notes=notes or APPROVED_WITHOUT_CHANGES,
        reviewed_at=reviewed_at,
    )


def edit_evidence(
    path: Path,
    evidence_id: str,
    reviewed_text: str,
    reviewer: str,
    notes: str | None = None,
    reviewed_at: str | None = None,
) -> dict[str, Any]:
    return update_review_node(
        path,
        evidence_id,
        review_status="human_reviewed",
        reviewer=reviewer,
        reviewed_text=reviewed_text,
        notes=notes,
        reviewed_at=reviewed_at,
    )


def reject_evidence(
    path: Path,
    evidence_id: str,
    reviewer: str,
    notes: str | None = None,
    reviewed_at: str | None = None,
) -> dict[str, Any]:
    return update_review_node(
        path,
        evidence_id,
        review_status="rejected",
        reviewer=reviewer,
        notes=notes,
        reviewed_at=reviewed_at,
    )


def review_stats(payload: dict[str, Any]) -> dict[str, int]:
    counts = {
        "total": 0,
        "unreviewed": 0,
        "human_reviewed": 0,
        "rejected": 0,
    }

    for node in evidence_nodes(payload):
        counts["total"] += 1
        status = str(node.get("review_status", "unreviewed"))
        if status in counts:
            counts[status] += 1

    return counts


def format_stats(counts: dict[str, int]) -> str:
    return "\n".join(
        [
            f"total Evidence: {counts['total']}",
            f"unreviewed: {counts['unreviewed']}",
            f"human_reviewed: {counts['human_reviewed']}",
            f"rejected: {counts['rejected']}",
        ]
    )


def stats_review_queue(path: Path) -> str:
    return format_stats(review_stats(load_json(path)))


def add_path_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--path",
        type=Path,
        default=DEFAULT_REVIEW_PATH,
        help="Review queue JSON path.",
    )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Review batch Evidence nodes from the command line."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a review queue.")
    init_parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="Processed Evidence batch JSON path.",
    )
    init_parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_REVIEW_PATH,
        help="Review queue output JSON path.",
    )

    list_parser = subparsers.add_parser("list", help="List Evidence review status.")
    add_path_argument(list_parser)

    show_parser = subparsers.add_parser("show", help="Show one Evidence node.")
    show_parser.add_argument("evidence_id")
    add_path_argument(show_parser)

    approve_parser = subparsers.add_parser("approve", help="Approve Evidence.")
    approve_parser.add_argument("evidence_id")
    approve_parser.add_argument("--reviewer", required=True)
    approve_parser.add_argument("--notes")
    add_path_argument(approve_parser)

    edit_parser = subparsers.add_parser("edit", help="Edit and approve Evidence.")
    edit_parser.add_argument("evidence_id")
    edit_parser.add_argument("--text", required=True)
    edit_parser.add_argument("--reviewer", required=True)
    edit_parser.add_argument("--notes")
    add_path_argument(edit_parser)

    reject_parser = subparsers.add_parser("reject", help="Reject Evidence.")
    reject_parser.add_argument("evidence_id")
    reject_parser.add_argument("--reviewer", required=True)
    reject_parser.add_argument("--notes")
    add_path_argument(reject_parser)

    stats_parser = subparsers.add_parser("stats", help="Count review statuses.")
    add_path_argument(stats_parser)

    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    if args.command == "init":
        queue = init_review_queue(args.input, args.output)
        print(
            f"Wrote {args.output} with {len(evidence_nodes(queue))} Evidence node(s)."
        )
        return 0

    if args.command == "list":
        print(list_review_queue(args.path))
        return 0

    if args.command == "show":
        print(show_evidence(args.path, args.evidence_id))
        return 0

    if args.command == "approve":
        approve_evidence(args.path, args.evidence_id, args.reviewer, args.notes)
        print(f"Approved {args.evidence_id}.")
        return 0

    if args.command == "edit":
        edit_evidence(
            args.path,
            args.evidence_id,
            reviewed_text=args.text,
            reviewer=args.reviewer,
            notes=args.notes,
        )
        print(f"Edited and approved {args.evidence_id}.")
        return 0

    if args.command == "reject":
        reject_evidence(args.path, args.evidence_id, args.reviewer, args.notes)
        print(f"Rejected {args.evidence_id}.")
        return 0

    if args.command == "stats":
        print(stats_review_queue(args.path))
        return 0

    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
