#!/usr/bin/env python3
"""Manage the Dharma Knowledge Graph Source Registry."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

DEFAULT_REGISTRY_PATH = Path("data") / "registry" / "sources.json"
VALID_SOURCE_KINDS = {"youtube"}
REQUIRED_FIELDS = (
    "source_id",
    "corpus_id",
    "title",
    "speaker",
    "source_kind",
    "source_url",
    "language",
    "status",
    "ingestion_status",
    "review_status",
    "curation_status",
    "index_status",
    "health_status",
)
PATH_FIELDS = (
    "raw_paths",
    "processed_paths",
    "reviewed_paths",
    "curated_paths",
    "index_paths",
)


def current_local_iso_datetime() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load_registry(path: Path = DEFAULT_REGISTRY_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_registry(path: Path, registry: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(registry, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def sources(registry: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        source for source in registry.get("sources", []) if isinstance(source, dict)
    ]


def source_by_id(registry: dict[str, Any], source_id: str) -> dict[str, Any] | None:
    for source in sources(registry):
        if source.get("source_id") == source_id:
            return source
    return None


def validate_registry_path(path: Path = DEFAULT_REGISTRY_PATH) -> list[str]:
    if not path.exists():
        return [f"Registry file missing: {path}"]

    try:
        registry = load_registry(path)
    except json.JSONDecodeError as error:
        return [f"Invalid JSON: {error}"]

    return validate_registry(registry)


def validate_registry(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    seen_source_ids: set[str] = set()

    if not isinstance(registry.get("sources"), list):
        errors.append("sources must be a list")
        return errors

    for index, source in enumerate(sources(registry)):
        source_label = str(source.get("source_id") or f"source[{index}]")

        for field in REQUIRED_FIELDS:
            if not str(source.get(field, "")).strip():
                errors.append(f"{source_label} missing required field: {field}")

        source_id = str(source.get("source_id", ""))
        if source_id in seen_source_ids:
            errors.append(f"duplicate source_id: {source_id}")
        seen_source_ids.add(source_id)

        if source.get("source_kind") not in VALID_SOURCE_KINDS:
            errors.append(
                f"{source_label} invalid source_kind: {source.get('source_kind')}"
            )

        for field in PATH_FIELDS:
            value = source.get(field, [])
            if not isinstance(value, list):
                errors.append(f"{source_label} {field} must be a list")
                continue
            if len(value) != len(set(value)):
                errors.append(f"{source_label} {field} contains duplicate paths")

    return errors


def format_list(registry: dict[str, Any]) -> str:
    lines = [
        "source_id | title | speaker | status | ingestion_status | review_status | curation_status | health_status"
    ]
    for source in sources(registry):
        lines.append(
            " | ".join(
                [
                    str(source.get("source_id", "")),
                    str(source.get("title", "")),
                    str(source.get("speaker", "")),
                    str(source.get("status", "")),
                    str(source.get("ingestion_status", "")),
                    str(source.get("review_status", "")),
                    str(source.get("curation_status", "")),
                    str(source.get("health_status", "")),
                ]
            )
        )
    return "\n".join(lines)


def list_sources(path: Path = DEFAULT_REGISTRY_PATH) -> str:
    return format_list(load_registry(path))


def format_source(source: dict[str, Any]) -> str:
    lines: list[str] = []
    for key in sorted(source):
        value = source[key]
        if isinstance(value, list):
            lines.append(f"{key}:")
            lines.extend(f"  - {item}" for item in value)
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines)


def show_source(source_id: str, path: Path = DEFAULT_REGISTRY_PATH) -> str:
    registry = load_registry(path)
    source = source_by_id(registry, source_id)
    if source is None:
        raise ValueError(f"Source not found: {source_id}")
    return format_source(source)


def default_youtube_source(args: argparse.Namespace) -> dict[str, Any]:
    now = current_local_iso_datetime()
    return {
        "source_id": args.source_id,
        "corpus_id": args.corpus_id,
        "title": args.title,
        "speaker": args.speaker,
        "source_owner": args.source_owner,
        "source_kind": "youtube",
        "source_url": args.url,
        "video_id": args.video_id,
        "language": args.language,
        "topic": args.topic,
        "status": "planned",
        "ingestion_status": "pending",
        "review_status": "not_started",
        "curation_status": "not_started",
        "index_status": "not_indexed",
        "health_status": "unknown",
        "raw_paths": [],
        "processed_paths": [],
        "reviewed_paths": [],
        "curated_paths": [],
        "index_paths": [],
        "notes": "",
        "created_at": now,
        "updated_at": now,
    }


def add_youtube_source(
    args: argparse.Namespace,
    path: Path = DEFAULT_REGISTRY_PATH,
) -> dict[str, Any]:
    registry = load_registry(path)
    if source_by_id(registry, args.source_id) is not None:
        raise ValueError(f"Duplicate source_id: {args.source_id}")

    registry.setdefault("sources", []).append(default_youtube_source(args))
    registry.setdefault("metadata", {})["updated_at"] = current_local_iso_datetime()
    write_registry(path, registry)
    return registry


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage the DKG Source Registry.")
    parser.add_argument(
        "--path",
        type=Path,
        default=DEFAULT_REGISTRY_PATH,
        help="Source registry JSON path.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List registered sources.")

    show_parser = subparsers.add_parser("show", help="Show one source.")
    show_parser.add_argument("source_id")

    subparsers.add_parser("validate", help="Validate source registry.")

    add_parser = subparsers.add_parser("add-youtube", help="Add a YouTube source.")
    add_parser.add_argument("--source-id", required=True)
    add_parser.add_argument("--video-id", required=True)
    add_parser.add_argument("--url", required=True)
    add_parser.add_argument("--title", required=True)
    add_parser.add_argument("--speaker", required=True)
    add_parser.add_argument("--source-owner", default="")
    add_parser.add_argument("--topic", required=True)
    add_parser.add_argument("--language", required=True)
    add_parser.add_argument("--corpus-id", required=True)

    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        if args.command == "list":
            print(list_sources(args.path))
            return 0

        if args.command == "show":
            print(show_source(args.source_id, args.path))
            return 0

        if args.command == "validate":
            errors = validate_registry_path(args.path)
            if errors:
                print("Source Registry: FAIL")
                for error in errors:
                    print(f"- {error}")
                return 1
            print("Source Registry: PASS")
            return 0

        if args.command == "add-youtube":
            add_youtube_source(args, args.path)
            print(f"Added source: {args.source_id}")
            return 0

    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Error: {error}")
        return 1

    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
