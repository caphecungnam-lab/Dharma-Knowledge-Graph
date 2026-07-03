#!/usr/bin/env python3
"""Plan or run the source pipeline for a registered Giac Khang source."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dharma_kg.registry import find_source, load_registry  # noqa: E402

DEFAULT_REGISTRY_PATH = Path("data") / "registry" / "sources.json"
DEFAULT_CORPUS_DIR = Path("data") / "raw" / "giac_khang"
DEFAULT_PROCESSED_DIR = Path("data") / "processed" / "giac_khang"
DEFAULT_REVIEWED_DIR = Path("data") / "reviewed" / "giac_khang"
DEFAULT_CURATED_DIR = Path("data") / "curated" / "giac_khang"
DEFAULT_INDEX_PATH = (
    Path("data") / "indexes" / "giac_khang" / "curated_evidence_index.json"
)


@dataclass(frozen=True)
class PipelinePaths:
    raw_vtt: Path
    processed_batch: Path
    review_queue: Path
    curated_batch: Path
    curated_index: Path


@dataclass(frozen=True)
class PipelineStep:
    name: str
    command: list[str]
    output_path: Path | None = None
    skip_if_exists: bool = False


def path_string(path: Path) -> str:
    return path.as_posix()


def source_video_id(source: dict[str, Any]) -> str:
    video_id = str(source.get("video_id", "")).strip()
    if not video_id:
        raise ValueError("Source is missing video_id.")
    return video_id


def source_language(source: dict[str, Any]) -> str:
    return str(source.get("language", "")).strip() or "vi"


def source_ids(registry: dict[str, Any]) -> list[str]:
    return [
        str(source.get("source_id"))
        for source in registry.get("sources", [])
        if isinstance(source, dict) and source.get("source_id")
    ]


def pipeline_paths(source: dict[str, Any]) -> PipelinePaths:
    video_id = source_video_id(source)
    language = source_language(source)
    return PipelinePaths(
        raw_vtt=DEFAULT_CORPUS_DIR / video_id / f"source.{language}.vtt",
        processed_batch=DEFAULT_PROCESSED_DIR / video_id / "evidence_batch_001.json",
        review_queue=DEFAULT_REVIEWED_DIR
        / video_id
        / "evidence_batch_001_review_queue.json",
        curated_batch=DEFAULT_CURATED_DIR
        / video_id
        / "evidence_batch_001_curated.json",
        curated_index=DEFAULT_INDEX_PATH,
    )


def build_pipeline_steps(
    source_id: str,
    source: dict[str, Any],
    paths: PipelinePaths,
    limit: int,
    start_time: str | None,
    end_time: str | None,
    force: bool,
    no_check_certificates: bool,
    update_registry: bool,
    cookies: Path | None,
) -> list[PipelineStep]:
    download_command = [
        sys.executable,
        "scripts/download_transcript.py",
        source_id,
        "--output",
        path_string(paths.raw_vtt),
    ]
    if force:
        download_command.append("--force")
    if no_check_certificates:
        download_command.append("--no-check-certificates")
    if update_registry:
        download_command.append("--update-registry")
    if cookies is not None:
        download_command.extend(["--cookies", path_string(cookies)])

    ingest_command = [
        sys.executable,
        "scripts/vtt_to_evidence.py",
        path_string(paths.raw_vtt),
        "--limit",
        str(limit),
        "--output",
        path_string(paths.processed_batch),
    ]
    if start_time:
        ingest_command.extend(["--start-time", start_time])
    if end_time:
        ingest_command.extend(["--end-time", end_time])

    return [
        PipelineStep(
            name="Download transcript",
            command=download_command,
            output_path=paths.raw_vtt,
            skip_if_exists=True,
        ),
        PipelineStep(
            name="Build processed Evidence batch",
            command=ingest_command,
            output_path=paths.processed_batch,
            skip_if_exists=not force,
        ),
        PipelineStep(
            name="Create review queue",
            command=[
                sys.executable,
                "scripts/batch_review_helper.py",
                "init",
                "--input",
                path_string(paths.processed_batch),
                "--output",
                path_string(paths.review_queue),
            ],
            output_path=paths.review_queue,
            skip_if_exists=not force,
        ),
        PipelineStep(
            name="Promote human-reviewed Evidence",
            command=[
                sys.executable,
                "scripts/promote_reviewed_evidence.py",
                "--input",
                path_string(paths.review_queue),
                "--output",
                path_string(paths.curated_batch),
            ],
            output_path=paths.curated_batch,
            skip_if_exists=False,
        ),
        PipelineStep(
            name="Rebuild curated index",
            command=[
                sys.executable,
                "scripts/build_curated_index.py",
                "--output",
                path_string(paths.curated_index),
            ],
            output_path=paths.curated_index,
            skip_if_exists=False,
        ),
    ]


def command_text(command: Sequence[str]) -> str:
    return " ".join(command)


def format_plan(
    source_id: str,
    source: dict[str, Any],
    paths: PipelinePaths,
    steps: list[PipelineStep],
    execute: bool,
) -> str:
    mode = "EXECUTE" if execute else "PREVIEW"
    lines = [
        f"Source Pipeline: {mode}",
        "",
        f"source_id: {source_id}",
        f"video_id: {source_video_id(source)}",
        f"title: {source.get('title', '')}",
        "",
        "Paths:",
        f"- raw_vtt: {path_string(paths.raw_vtt)}",
        f"- processed_batch: {path_string(paths.processed_batch)}",
        f"- review_queue: {path_string(paths.review_queue)}",
        f"- curated_batch: {path_string(paths.curated_batch)}",
        f"- curated_index: {path_string(paths.curated_index)}",
        "",
        "Steps:",
    ]
    for index, step in enumerate(steps, 1):
        lines.append(f"{index}. {step.name}")
        lines.append(f"   {command_text(step.command)}")

    if not execute:
        lines.extend(
            [
                "",
                "No files were changed.",
                "Run again with --execute to run the pipeline.",
            ]
        )
    return "\n".join(lines)


def run_step(step: PipelineStep, force: bool) -> None:
    if (
        step.skip_if_exists
        and step.output_path is not None
        and step.output_path.exists()
        and not force
    ):
        print(f"Skipping {step.name}: output already exists: {step.output_path}")
        return

    print(f"Running {step.name}...")
    completed = subprocess.run(step.command, check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"Step failed: {step.name}")


def run_pipeline(
    source_id: str,
    registry_path: Path = DEFAULT_REGISTRY_PATH,
    execute: bool = False,
    force: bool = False,
    limit: int = 50,
    start_time: str | None = None,
    end_time: str | None = "00:20:00",
    no_check_certificates: bool = False,
    update_registry: bool = False,
    cookies: Path | None = None,
) -> str:
    registry = load_registry(registry_path)
    source = find_source(registry, source_id)
    if source is None:
        available = ", ".join(source_ids(registry)) or "(none)"
        raise ValueError(
            f"Source not found: {source_id}. Available sources: {available}"
        )

    paths = pipeline_paths(source)
    steps = build_pipeline_steps(
        source_id=source_id,
        source=source,
        paths=paths,
        limit=limit,
        start_time=start_time,
        end_time=end_time,
        force=force,
        no_check_certificates=no_check_certificates,
        update_registry=update_registry,
        cookies=cookies,
    )
    plan = format_plan(source_id, source, paths, steps, execute=execute)

    if not execute:
        return plan

    print(plan)
    for step in steps:
        run_step(step, force=force)
    return "Source pipeline complete."


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preview or run the source pipeline for a registered source."
    )
    parser.add_argument("source_id")
    parser.add_argument("--registry-path", type=Path, default=DEFAULT_REGISTRY_PATH)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--start-time")
    parser.add_argument("--end-time", default="00:20:00")
    parser.add_argument("--no-check-certificates", action="store_true")
    parser.add_argument("--update-registry", action="store_true")
    parser.add_argument("--cookies", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        output = run_pipeline(
            source_id=args.source_id,
            registry_path=args.registry_path,
            execute=args.execute,
            force=args.force,
            limit=args.limit,
            start_time=args.start_time,
            end_time=args.end_time,
            no_check_certificates=args.no_check_certificates,
            update_registry=args.update_registry,
            cookies=args.cookies,
        )
        print(output)
        return 0
    except (OSError, RuntimeError, ValueError) as error:
        print(f"Error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
