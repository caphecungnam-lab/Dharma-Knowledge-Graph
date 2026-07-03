#!/usr/bin/env python3
"""Download YouTube transcript subtitles for a registered source."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dharma_kg.registry import (  # noqa: E402
    find_source,
    load_registry,
    save_registry,
    update_source_raw_path,
)

DEFAULT_REGISTRY_PATH = Path("data") / "registry" / "sources.json"
DEFAULT_BASE_RAW_DIR = Path("data") / "raw" / "giac_khang"


def current_local_iso_datetime() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def path_string(path: Path) -> str:
    return path.as_posix()


def default_output_path(source: dict[str, Any], language: str) -> Path:
    video_id = str(source.get("video_id", "")).strip()
    if not video_id:
        raise ValueError("Source is missing video_id")
    return DEFAULT_BASE_RAW_DIR / video_id / f"source.{language}.vtt"


def resolve_output_path(
    source: dict[str, Any],
    language: str,
    output: Path | None,
) -> Path:
    return output if output is not None else default_output_path(source, language)


def language_candidates(language: str) -> list[str]:
    candidates = [language]
    if language == "vi":
        candidates.extend(["vi-orig", "en"])

    unique: list[str] = []
    for candidate in candidates:
        if candidate not in unique:
            unique.append(candidate)
    return unique


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )


def detect_yt_dlp_command() -> list[str]:
    python_module_command = [sys.executable, "-m", "yt_dlp"]
    module_check = run_command([*python_module_command, "--version"])
    if module_check.returncode == 0:
        return python_module_command

    binary_path = shutil.which("yt-dlp")
    if binary_path:
        binary_check = run_command([binary_path, "--version"])
        if binary_check.returncode == 0:
            return [binary_path]

    raise RuntimeError(
        "yt-dlp is not available. Install it with: python3 -m pip install yt-dlp"
    )


def build_yt_dlp_command(
    yt_dlp_command: list[str],
    source_url: str,
    language: str,
    temp_dir: Path,
    no_check_certificates: bool = False,
) -> list[str]:
    command = [
        *yt_dlp_command,
        "--skip-download",
        "--write-auto-subs",
        "--sub-lang",
        language,
        "--sub-format",
        "vtt",
        "--output",
        path_string(temp_dir / "%(id)s.%(ext)s"),
    ]
    if no_check_certificates:
        command.append("--no-check-certificates")
    command.append(source_url)
    return command


def locate_downloaded_vtt(temp_dir: Path) -> Path | None:
    candidates = sorted(temp_dir.glob("*.vtt"))
    if not candidates:
        return None
    return candidates[0]


def clean_temp_dir(temp_dir: Path) -> None:
    if not temp_dir.exists():
        return
    for path in temp_dir.iterdir():
        if path.is_file():
            path.unlink()
    temp_dir.rmdir()


def copy_downloaded_transcript(
    downloaded_path: Path, final_path: Path, force: bool
) -> None:
    if final_path.exists() and not force:
        raise FileExistsError(f"Output already exists: {final_path}")
    final_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(downloaded_path, final_path)


def update_registry_after_download(
    registry_path: Path,
    registry: dict[str, Any],
    source_id: str,
    output_path: Path,
) -> None:
    source = find_source(registry, source_id)
    if source is None:
        raise ValueError(f"Source not found: {source_id}")

    now = current_local_iso_datetime()
    source["ingestion_status"] = "transcript_downloaded"
    source["updated_at"] = now
    update_source_raw_path(registry, source_id, path_string(output_path))
    registry.setdefault("metadata", {})["updated_at"] = now
    save_registry(registry_path, registry)


def download_transcript(
    source_id: str,
    registry_path: Path = DEFAULT_REGISTRY_PATH,
    output: Path | None = None,
    language: str | None = None,
    force: bool = False,
    dry_run: bool = False,
    no_check_certificates: bool = False,
    update_registry: bool = False,
    cookies: Path | None = None,
) -> dict[str, Any]:
    registry = load_registry(registry_path)
    source = find_source(registry, source_id)
    if source is None:
        raise ValueError(f"Source not found: {source_id}")
    if source.get("source_kind") != "youtube":
        raise ValueError(f"Source is not youtube: {source_id}")

    source_url = str(source.get("source_url", "")).strip()
    video_id = str(source.get("video_id", "")).strip()
    selected_language = language or str(source.get("language", "")).strip() or "vi"
    final_output = resolve_output_path(source, selected_language, output)
    temp_dir = final_output.parent / ".tmp_download"

    if final_output.exists() and not force and not dry_run:
        raise FileExistsError(f"Output already exists: {final_output}")

    commands = []
    for candidate_language in language_candidates(selected_language):
        commands.append(
            build_yt_dlp_command(
                ["python3", "-m", "yt_dlp"],
                source_url,
                candidate_language,
                temp_dir,
                no_check_certificates=no_check_certificates,
            )
        )

    if dry_run:
        return {
            "source_id": source_id,
            "video_id": video_id,
            "source_url": source_url,
            "output": path_string(final_output),
            "language": selected_language,
            "dry_run": True,
            "commands": commands,
        }

    yt_dlp_command = detect_yt_dlp_command()
    temp_dir.mkdir(parents=True, exist_ok=True)

    last_error = ""
    try:
        for candidate_language in language_candidates(selected_language):
            for existing in temp_dir.glob("*"):
                if existing.is_file():
                    existing.unlink()

            command = build_yt_dlp_command(
                yt_dlp_command,
                source_url,
                candidate_language,
                temp_dir,
                no_check_certificates=no_check_certificates,
            )
            if cookies is not None:
                command.insert(-1, "--cookies")
                command.insert(-1, path_string(cookies))

            completed = run_command(command)
            if completed.returncode != 0:
                last_error = completed.stderr.strip() or completed.stdout.strip()
                continue

            downloaded_path = locate_downloaded_vtt(temp_dir)
            if downloaded_path is None:
                last_error = f"No VTT subtitle found for language: {candidate_language}"
                continue

            copy_downloaded_transcript(downloaded_path, final_output, force=force)
            if update_registry:
                update_registry_after_download(
                    registry_path,
                    registry,
                    source_id,
                    final_output,
                )

            return {
                "source_id": source_id,
                "video_id": video_id,
                "source_url": source_url,
                "output": path_string(final_output),
                "language": selected_language,
                "downloaded_language": candidate_language,
                "dry_run": False,
            }

    finally:
        clean_temp_dir(temp_dir)

    raise RuntimeError(f"Transcript download failed. {last_error}".strip())


def format_result(result: dict[str, Any]) -> str:
    lines = [
        "Transcript Download Helper",
        "",
        f"source_id: {result['source_id']}",
        f"video_id: {result['video_id']}",
        f"source_url: {result['source_url']}",
        f"output: {result['output']}",
        f"language: {result['language']}",
    ]

    if result.get("dry_run"):
        lines.append("dry_run: true")
        lines.append("")
        lines.append("Commands:")
        for command in result.get("commands", []):
            lines.append("- " + " ".join(command))
    else:
        lines.append(f"downloaded_language: {result['downloaded_language']}")
        if result["downloaded_language"] != result["language"]:
            lines.append("note: fallback subtitle language was used")

    return "\n".join(lines)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download source transcript subtitles."
    )
    parser.add_argument("source_id")
    parser.add_argument("--registry-path", type=Path, default=DEFAULT_REGISTRY_PATH)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--language")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-check-certificates", action="store_true")
    parser.add_argument("--update-registry", action="store_true")
    parser.add_argument("--cookies", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = download_transcript(
            source_id=args.source_id,
            registry_path=args.registry_path,
            output=args.output,
            language=args.language,
            force=args.force,
            dry_run=args.dry_run,
            no_check_certificates=args.no_check_certificates,
            update_registry=args.update_registry,
            cookies=args.cookies,
        )
        print(format_result(result))
        return 0
    except (
        FileExistsError,
        OSError,
        RuntimeError,
        ValueError,
        json.JSONDecodeError,
    ) as error:
        print(f"Error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
