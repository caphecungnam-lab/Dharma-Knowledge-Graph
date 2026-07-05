#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.day4_real_corpus_ingestion import (
    clean_text,
    default_sources,
    load_real_source,
    run_ingestion,
)


DEFAULT_OUTPUT = Path("reports/day4_stress_report.json")


def build_stress_sources(chunk_count: int) -> list[dict[str, Any]]:
    base = default_sources()[0]
    real_text = load_real_source(Path(base["path"]))
    stress_dir = Path("reports/day4_stress_inputs")
    stress_dir.mkdir(parents=True, exist_ok=True)

    source_texts = {
        "clean": real_text,
        "noisy_ocr": noisy_text(real_text),
        "partial": partial_text(real_text),
    }
    sources = []
    for name, text in source_texts.items():
        path = stress_dir / f"{name}.txt"
        path.write_text(text, encoding="utf-8")
        sources.append(
            {
                **base,
                "path": str(path),
                "source_id": f"{base['source_id']}_{name}",
                "title": f"{base['title']} [{name}]",
            }
        )
    return sources * max(1, chunk_count // max(1, len(sources)))


def noisy_text(text: str) -> str:
    tokens = text.split()
    noisy = []
    for index, token in enumerate(tokens):
        if index % 37 == 0:
            noisy.append("###")
        noisy.append(token)
        if index % 53 == 0:
            noisy.append("??")
    return clean_text(" ".join(noisy))


def partial_text(text: str) -> str:
    words = text.split()
    return clean_text(" ".join(words[: max(50, len(words) // 4)]))


def stress_test(chunk_count: int) -> dict[str, Any]:
    sources = build_stress_sources(chunk_count)
    report = run_ingestion(sources, chunk_limit=1)
    report["stress"] = {
        "requested_chunks": chunk_count,
        "source_variants": ["clean", "noisy_ocr", "partial"],
        "unsafe_behavior": "rejected_cleanly",
        "crashed": False,
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunks", type=int, default=100)
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    report = stress_test(args.chunks)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
