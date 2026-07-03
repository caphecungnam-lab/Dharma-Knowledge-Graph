from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
SOURCES_DIR = DATA_DIR / "sources"
PIPELINE_LOG_DIR = DATA_DIR / "pipeline_logs"


@dataclass
class PipelineResult:
    step: str
    ok: bool
    detail: str = ""


def run_cmd(cmd: list[str], required: bool = True) -> PipelineResult:
    try:
        completed = subprocess.run(
            cmd,
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        ok = completed.returncode == 0
        detail = (completed.stdout or completed.stderr or "").strip()

        if required and not ok:
            return PipelineResult(
                step=" ".join(cmd),
                ok=False,
                detail=detail,
            )

        return PipelineResult(
            step=" ".join(cmd),
            ok=ok,
            detail=detail,
        )

    except FileNotFoundError as exc:
        return PipelineResult(
            step=" ".join(cmd),
            ok=not required,
            detail=str(exc),
        )


def ensure_dirs() -> None:
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    PIPELINE_LOG_DIR.mkdir(parents=True, exist_ok=True)


def detect_source_type(source: str) -> str:
    lowered = source.lower()

    if "youtube.com" in lowered or "youtu.be" in lowered:
        return "youtube"

    if lowered.endswith(".txt"):
        return "text"

    if lowered.endswith(".md"):
        return "markdown"

    if lowered.endswith(".json"):
        return "json"

    if lowered.startswith("http://") or lowered.startswith("https://"):
        return "web"

    return "local"


def write_source_manifest(source: str, teacher: str, title: str | None = None) -> Path:
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    source_type = detect_source_type(source)

    manifest = {
        "id": f"{teacher}_{source_type}_{now}",
        "teacher": teacher,
        "title": title or "",
        "source": source,
        "source_type": source_type,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "registered",
    }

    path = SOURCES_DIR / f"{manifest['id']}.json"

    with path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    return path


def candidate_commands(manifest_path: Path, teacher: str) -> list[tuple[str, list[str], bool]]:
    """
    Chạy theo kiểu mềm: nếu repo đã có script nào thì dùng script đó.
    Truyền đúng CLI hiện có của từng script, không giả định script nào cũng nhận --teacher.
    """

    candidates: list[tuple[str, list[str], bool]] = []

    curated_index = DATA_DIR / "indexes" / teacher / "curated_evidence_index.json"
    dashboard_md = DATA_DIR / "dashboards" / teacher / "corpus_dashboard.md"
    dashboard_json = DATA_DIR / "dashboards" / teacher / "corpus_dashboard.json"

    possible_steps = [
        (
            "ingest",
            ROOT / "scripts" / "ingest_source.py",
            [
                sys.executable,
                str(ROOT / "scripts" / "ingest_source.py"),
                "--manifest",
                str(manifest_path),
            ],
            False,
        ),
        (
            "build-evidence-index",
            ROOT / "scripts" / "build_curated_evidence_index.py",
            [
                sys.executable,
                str(ROOT / "scripts" / "build_curated_evidence_index.py"),
            ],
            False,
        ),
        (
            "build-corpus-dashboard",
            ROOT / "scripts" / "build_corpus_dashboard.py",
            [
                sys.executable,
                str(ROOT / "scripts" / "build_corpus_dashboard.py"),
                "--input",
                str(curated_index),
                "--output-md",
                str(dashboard_md),
                "--output-json",
                str(dashboard_json),
            ],
            False,
        ),
        (
            "corpus-health",
            ROOT / "scripts" / "check_corpus_health.py",
            [
                sys.executable,
                str(ROOT / "scripts" / "check_corpus_health.py"),
                "--input",
                str(curated_index),
            ],
            False,
        ),
    ]

    for name, path, cmd, required in possible_steps:
        if path.exists():
            candidates.append((name, cmd, required))

    return candidates


def write_pipeline_log(results: list[PipelineResult], manifest_path: Path) -> Path:
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = PIPELINE_LOG_DIR / f"source_pipeline_{now}.json"

    payload = {
        "manifest": str(manifest_path.relative_to(ROOT)),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "results": [
            {
                "step": r.step,
                "ok": r.ok,
                "detail": r.detail,
            }
            for r in results
        ],
        "ok": all(r.ok for r in results),
    }

    with log_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return log_path


def run_pipeline(source: str, teacher: str, title: str | None = None) -> int:
    ensure_dirs()

    results: list[PipelineResult] = []

    manifest_path = write_source_manifest(source=source, teacher=teacher, title=title)
    results.append(
        PipelineResult(
            step="register-source",
            ok=True,
            detail=str(manifest_path.relative_to(ROOT)),
        )
    )

    commands = candidate_commands(manifest_path=manifest_path, teacher=teacher)

    if not commands:
        results.append(
            PipelineResult(
                step="pipeline-steps",
                ok=True,
                detail="No existing scripts found. Source manifest registered only.",
            )
        )
    else:
        for name, cmd, required in commands:
            result = run_cmd(cmd, required=required)
            result.step = name
            results.append(result)

            if required and not result.ok:
                break

    log_path = write_pipeline_log(results, manifest_path)

    print("\nDKG Source Pipeline")
    print("=" * 40)
    print(f"Source   : {source}")
    print(f"Teacher  : {teacher}")
    print(f"Manifest : {manifest_path.relative_to(ROOT)}")
    print(f"Log      : {log_path.relative_to(ROOT)}")
    print("-" * 40)

    for result in results:
        icon = "PASS" if result.ok else "FAIL"
        print(f"{icon} {result.step}")
        if result.detail:
            print(f"     {result.detail[:500]}")

    if all(r.ok for r in results):
        print("\nPipeline completed.")
        return 0

    print("\nPipeline failed.")
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="One-command source pipeline for Dharma Knowledge Graph."
    )

    parser.add_argument(
        "--source",
        required=True,
        help="Source URL or local source path.",
    )

    parser.add_argument(
        "--teacher",
        default="giac_khang",
        help="Teacher/corpus namespace. Default: giac_khang.",
    )

    parser.add_argument(
        "--title",
        default=None,
        help="Optional human-readable source title.",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    return run_pipeline(
        source=args.source,
        teacher=args.teacher,
        title=args.title,
    )


if __name__ == "__main__":
    raise SystemExit(main())
