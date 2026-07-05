#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


DEFAULT_INPUT = Path("reports/day4_corpus_report.json")


def detect_drift(report: dict[str, Any]) -> dict[str, Any]:
    concepts: dict[str, dict[str, set[str]]] = defaultdict(
        lambda: {"traditions": set(), "definitions": set(), "types": set()}
    )
    confidence_spikes = []

    for document in report.get("documents", []):
        for node in document.get("accepted_nodes", []):
            concept = str(node.get("node_id") or "")
            match = node.get("match") or {}
            concepts[concept]["traditions"].add(str(node.get("tradition") or "unknown"))
            concepts[concept]["definitions"].add(str(match.get("definition") or match.get("text") or ""))
            concepts[concept]["types"].add(str(node.get("epistemic_type") or "unknown"))
            if float(node.get("confidence") or 0.0) > 0.95:
                confidence_spikes.append(concept)

    affected = []
    for concept, values in concepts.items():
        if (
            len(values["traditions"]) > 1
            or len(values["definitions"]) > 1
            or len(values["types"]) > 1
            or concept in confidence_spikes
        ):
            affected.append(concept)

    severity = "low"
    if len(affected) >= 5:
        severity = "high"
    elif affected:
        severity = "medium"

    return {
        "drift_detected": bool(affected),
        "affected_concepts": sorted(set(affected)),
        "severity": severity,
        "confidence_spikes": sorted(set(confidence_spikes)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output")
    args = parser.parse_args()

    report = json.loads(Path(args.input).read_text(encoding="utf-8"))
    drift = detect_drift(report)
    if args.output:
        Path(args.output).write_text(
            json.dumps(drift, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    print(json.dumps(drift, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
