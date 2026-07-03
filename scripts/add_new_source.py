#!/usr/bin/env python3
"""Register and scaffold a new Giac Khang source."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dharma_kg.youtube import (
    extract_youtube_video_id,
    normalize_youtube_url,
)  # noqa: E402

DEFAULT_REGISTRY_PATH = Path("data") / "registry" / "sources.json"
DEFAULT_BASE_RAW_DIR = Path("data") / "raw" / "giac_khang"
DEFAULT_BASE_PROCESSED_DIR = Path("data") / "processed" / "giac_khang"
DEFAULT_BASE_REVIEWED_DIR = Path("data") / "reviewed" / "giac_khang"
DEFAULT_BASE_CURATED_DIR = Path("data") / "curated" / "giac_khang"
DEFAULT_SOURCE_OWNER = "PHÁP ÂM SƯ KHANG"
README_TEXT = """# Source Workspace

This directory was created by `scripts/add_new_source.py`.

Add source-specific files here as the pipeline progresses.
"""


def current_local_iso_datetime() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def source_id_for_video(video_id: str) -> str:
    return f"source_youtube_{video_id.lower()}"


def load_registry(path: Path) -> dict[str, Any]:
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


def source_exists(registry: dict[str, Any], source_id: str) -> bool:
    return any(source.get("source_id") == source_id for source in sources(registry))


def video_id_exists(registry: dict[str, Any], video_id: str) -> bool:
    return any(source.get("video_id") == video_id for source in sources(registry))


def source_directories(args: argparse.Namespace, video_id: str) -> dict[str, Path]:
    return {
        "raw": args.base_raw_dir / video_id,
        "processed": args.base_processed_dir / video_id,
        "reviewed": args.base_reviewed_dir / video_id,
        "curated": args.base_curated_dir / video_id,
    }


def path_string(path: Path) -> str:
    return path.as_posix()


def build_source_entry(
    args: argparse.Namespace,
    source_id: str,
    video_id: str,
    normalized_url: str,
    directories: dict[str, Path],
) -> dict[str, Any]:
    now = current_local_iso_datetime()
    return {
        "source_id": source_id,
        "corpus_id": args.corpus_id,
        "title": args.title,
        "speaker": args.speaker,
        "source_owner": args.source_owner,
        "source_kind": "youtube",
        "source_url": normalized_url,
        "video_id": video_id,
        "language": args.language,
        "topic": args.topic,
        "status": "planned",
        "ingestion_status": "pending",
        "review_status": "not_started",
        "curation_status": "not_started",
        "index_status": "not_indexed",
        "health_status": "unknown",
        "raw_paths": [path_string(directories["raw"]) + "/"],
        "processed_paths": [path_string(directories["processed"]) + "/"],
        "reviewed_paths": [path_string(directories["reviewed"]) + "/"],
        "curated_paths": [path_string(directories["curated"]) + "/"],
        "index_paths": [],
        "notes": "Registered source. Awaiting transcript ingestion.",
        "created_at": now,
        "updated_at": now,
    }


def ensure_safe_to_write(directories: dict[str, Path]) -> None:
    for directory in directories.values():
        readme_path = directory / "README.md"
        if readme_path.exists():
            raise ValueError(f"Refusing to overwrite existing file: {readme_path}")


def write_scaffold(directories: dict[str, Path]) -> None:
    ensure_safe_to_write(directories)
    for directory in directories.values():
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "README.md").write_text(README_TEXT, encoding="utf-8")


def next_commands(video_id: str, directories: dict[str, Path]) -> list[str]:
    raw_vtt = directories["raw"] / "source.vi.vtt"
    processed_batch = directories["processed"] / "evidence_batch_001.json"
    review_queue = directories["reviewed"] / "evidence_batch_001_review_queue.json"
    return [
        f"Download transcript to: {path_string(raw_vtt)}",
        (
            "PYTHONPATH=src python3 scripts/vtt_to_evidence.py "
            f"{path_string(raw_vtt)} --limit 50 --output {path_string(processed_batch)}"
        ),
        (
            "PYTHONPATH=src python3 scripts/batch_review_helper.py init "
            f"--input {path_string(processed_batch)} --output {path_string(review_queue)}"
        ),
        "Review, promote, build index, dashboard, and health.",
    ]


def format_result(
    source_entry: dict[str, Any],
    directories: dict[str, Path],
    dry_run: bool,
) -> str:
    mode = "DRY RUN" if dry_run else "CREATED"
    lines = [
        f"Add New Source Workflow: {mode}",
        "",
        f"source_id: {source_entry['source_id']}",
        f"video_id: {source_entry['video_id']}",
        f"source_url: {source_entry['source_url']}",
        "",
        "Folders:",
    ]
    lines.extend(f"- {path_string(path)}/" for path in directories.values())
    lines.extend(["", "Next commands:"])
    for index, command in enumerate(
        next_commands(source_entry["video_id"], directories), 1
    ):
        lines.append(f"{index}. {command}")
    return "\n".join(lines)


def add_youtube_source(args: argparse.Namespace) -> tuple[dict[str, Any], str]:
    video_id = extract_youtube_video_id(args.url)
    normalized_url = normalize_youtube_url(args.url)
    if not video_id or not normalized_url:
        raise ValueError(f"Unsupported YouTube URL: {args.url}")

    source_id = source_id_for_video(video_id)
    registry = load_registry(args.registry_path)
    if source_exists(registry, source_id):
        raise ValueError(f"source_id already exists: {source_id}")
    if video_id_exists(registry, video_id) and not args.allow_duplicate_video_id:
        raise ValueError(f"video_id already exists: {video_id}")

    directories = source_directories(args, video_id)
    source_entry = build_source_entry(
        args, source_id, video_id, normalized_url, directories
    )

    if not args.dry_run:
        write_scaffold(directories)
        registry.setdefault("sources", []).append(source_entry)
        registry.setdefault("metadata", {})["updated_at"] = current_local_iso_datetime()
        write_registry(args.registry_path, registry)

    return source_entry, format_result(source_entry, directories, args.dry_run)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Register and scaffold a new source.")
    subparsers = parser.add_subparsers(dest="source_kind", required=True)

    youtube = subparsers.add_parser("youtube", help="Add a YouTube source.")
    youtube.add_argument("--url", required=True)
    youtube.add_argument("--title", required=True)
    youtube.add_argument("--speaker", required=True)
    youtube.add_argument("--topic", required=True)
    youtube.add_argument("--language", default="vi")
    youtube.add_argument("--corpus-id", default="corpus_giac_khang")
    youtube.add_argument("--source-owner", default=DEFAULT_SOURCE_OWNER)
    youtube.add_argument("--registry-path", type=Path, default=DEFAULT_REGISTRY_PATH)
    youtube.add_argument("--base-raw-dir", type=Path, default=DEFAULT_BASE_RAW_DIR)
    youtube.add_argument(
        "--base-processed-dir",
        type=Path,
        default=DEFAULT_BASE_PROCESSED_DIR,
    )
    youtube.add_argument(
        "--base-reviewed-dir",
        type=Path,
        default=DEFAULT_BASE_REVIEWED_DIR,
    )
    youtube.add_argument(
        "--base-curated-dir",
        type=Path,
        default=DEFAULT_BASE_CURATED_DIR,
    )
    youtube.add_argument("--allow-duplicate-video-id", action="store_true")
    youtube.add_argument("--dry-run", action="store_true")

    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        if args.source_kind == "youtube":
            _source_entry, output = add_youtube_source(args)
            print(output)
            return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Error: {error}")
        return 1

    raise ValueError(f"Unsupported source kind: {args.source_kind}")


if __name__ == "__main__":
    raise SystemExit(main())
