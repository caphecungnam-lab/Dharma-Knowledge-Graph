#!/usr/bin/env python3
"""Read-only corpus health gate for the curated Evidence index."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

DEFAULT_INPUT_PATH = (
    Path("data") / "indexes" / "giac_khang" / "curated_evidence_index.json"
)


def load_index(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    if not path.exists():
        return None, [f"Index file missing: {path}"]

    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except json.JSONDecodeError as error:
        return None, [f"Invalid JSON: {error}"]


def is_evidence_node(node: Any) -> bool:
    return isinstance(node, dict) and node.get("type") == "Evidence"


def evidence_nodes(payload: dict[str, Any] | None) -> list[dict[str, Any]]:
    if payload is None:
        return []
    return [node for node in payload.get("nodes", []) if is_evidence_node(node)]


def has_value(node: dict[str, Any], field: str) -> bool:
    return bool(str(node.get(field, "")).strip())


def quality_score(node: dict[str, Any]) -> int:
    try:
        return int(node.get("quality_score", 0))
    except (TypeError, ValueError):
        return 0


def ratio(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 4)


def duplicate_ids(nodes: list[dict[str, Any]]) -> list[str]:
    ids = [str(node.get("id", "")) for node in nodes]
    counts = Counter(ids)
    return sorted(node_id for node_id, count in counts.items() if node_id and count > 1)


def node_label(node: dict[str, Any]) -> str:
    return str(node.get("id", "(missing id)"))


def build_metrics(
    nodes: list[dict[str, Any]],
    min_quality: int,
) -> dict[str, Any]:
    duplicate_id_list = duplicate_ids(nodes)
    missing_citation_url = sum(
        1 for node in nodes if not has_value(node, "citation_url")
    )
    unreviewed = sum(
        1
        for node in nodes
        if node.get("review_status") not in {"human_reviewed", "verified"}
    )
    low_quality = sum(1 for node in nodes if quality_score(node) < min_quality)
    high_quality = sum(1 for node in nodes if quality_score(node) >= 80)
    total = len(nodes)

    return {
        "duplicate_ids": len(duplicate_id_list),
        "duplicate_id_values": duplicate_id_list,
        "missing_evidence_text": sum(
            1 for node in nodes if not has_value(node, "evidence_text")
        ),
        "missing_source_url": sum(
            1 for node in nodes if not has_value(node, "source_url")
        ),
        "missing_start_time": sum(
            1 for node in nodes if not has_value(node, "start_time")
        ),
        "missing_end_time": sum(1 for node in nodes if not has_value(node, "end_time")),
        "missing_citation_url": missing_citation_url,
        "missing_speaker": sum(1 for node in nodes if not has_value(node, "speaker")),
        "missing_evidence_type": sum(
            1 for node in nodes if not has_value(node, "evidence_type")
        ),
        "missing_confidence": sum(
            1 for node in nodes if not has_value(node, "confidence")
        ),
        "unreviewed": unreviewed,
        "not_curated": sum(
            1 for node in nodes if node.get("curated_status") != "curated"
        ),
        "low_quality": low_quality,
        "high_quality_ratio": ratio(high_quality, total),
        "missing_citation_ratio": ratio(missing_citation_url, total),
        "unreviewed_ratio": ratio(unreviewed, total),
    }


def add_missing_field_errors(
    nodes: list[dict[str, Any]],
    field: str,
    errors: list[str],
) -> None:
    for node in nodes:
        if not has_value(node, field):
            errors.append(f"{node_label(node)} missing {field}")


def add_missing_field_warnings(
    nodes: list[dict[str, Any]],
    field: str,
    warnings: list[str],
) -> None:
    for node in nodes:
        if not has_value(node, field):
            warnings.append(f"{node_label(node)} missing {field}")


def recommendations_for_result(
    metrics: dict[str, Any],
    evidence_count: int,
) -> list[str]:
    recommendations: list[str] = []

    if metrics["missing_citation_url"] > 0:
        recommendations.append("Rebuild the curated index to refresh citation URLs.")
    if metrics["unreviewed"] > 0:
        recommendations.append("Use batch_review_helper to review remaining Evidence.")
    if metrics["low_quality"] > 0:
        recommendations.append("Improve low-quality Evidence metadata before release.")
    if evidence_count == 0:
        recommendations.append("Build or restore the curated Evidence index.")

    return recommendations


def check_corpus_health(
    input_path: Path = DEFAULT_INPUT_PATH,
    strict: bool = False,
    min_quality: int = 50,
    min_high_quality_ratio: float = 0.0,
    max_missing_citation_ratio: float = 0.2,
    max_unreviewed_ratio: float = 0.2,
    max_duplicate_ids: int = 0,
) -> dict[str, Any]:
    payload, load_errors = load_index(input_path)
    nodes = evidence_nodes(payload)
    errors = list(load_errors)
    warnings: list[str] = []
    metrics = build_metrics(nodes, min_quality)

    if payload is not None and not nodes:
        errors.append("No Evidence nodes found.")

    if metrics["duplicate_ids"] > max_duplicate_ids:
        errors.append(
            "Duplicate Evidence ids count "
            f"{metrics['duplicate_ids']} exceeds max {max_duplicate_ids}: "
            + ", ".join(metrics["duplicate_id_values"])
        )

    for field in ["evidence_text", "source_url", "start_time", "end_time"]:
        add_missing_field_errors(nodes, field, errors)

    for node in nodes:
        if quality_score(node) < min_quality:
            errors.append(
                f"{node_label(node)} quality_score {quality_score(node)} "
                f"is below min {min_quality}"
            )

    for field in ["citation_url", "speaker", "evidence_type", "confidence"]:
        add_missing_field_warnings(nodes, field, warnings)

    for node in nodes:
        if node.get("review_status") not in {"human_reviewed", "verified"}:
            warnings.append(
                f"{node_label(node)} review_status is not human_reviewed or verified"
            )
        if node.get("curated_status") != "curated":
            warnings.append(f"{node_label(node)} curated_status is not curated")

    if metrics["high_quality_ratio"] < min_high_quality_ratio:
        warnings.append(
            "high_quality_ratio "
            f"{metrics['high_quality_ratio']} is below min {min_high_quality_ratio}"
        )
    if metrics["missing_citation_ratio"] > max_missing_citation_ratio:
        warnings.append(
            "missing_citation_ratio "
            f"{metrics['missing_citation_ratio']} exceeds max "
            f"{max_missing_citation_ratio}"
        )
    if metrics["unreviewed_ratio"] > max_unreviewed_ratio:
        warnings.append(
            f"unreviewed_ratio {metrics['unreviewed_ratio']} exceeds max "
            f"{max_unreviewed_ratio}"
        )

    failed = bool(errors) or (strict and bool(warnings))

    return {
        "status": "fail" if failed else "pass",
        "input": str(input_path),
        "evidence_count": len(nodes),
        "errors": errors,
        "warnings": warnings,
        "metrics": metrics,
        "recommendations": recommendations_for_result(metrics, len(nodes)),
    }


def format_health_report(result: dict[str, Any]) -> str:
    lines = [
        "Corpus Health Gate",
        "",
        f"Input: {result['input']}",
        f"Evidence count: {result['evidence_count']}",
        f"Status: {result['status'].upper()}",
        "",
        "Errors:",
    ]
    lines.extend(f"- {error}" for error in result["errors"] or ["None"])
    lines.extend(["", "Warnings:"])
    lines.extend(f"- {warning}" for warning in result["warnings"] or ["None"])
    lines.extend(["", "Metrics:"])
    metric_order = [
        "duplicate_ids",
        "missing_evidence_text",
        "missing_source_url",
        "missing_start_time",
        "missing_end_time",
        "missing_citation_url",
        "unreviewed",
        "not_curated",
        "low_quality",
        "high_quality_ratio",
        "missing_citation_ratio",
        "unreviewed_ratio",
    ]
    for key in metric_order:
        lines.append(f"- {key}: {result['metrics'].get(key, 0)}")

    lines.extend(["", "Recommendations:"])
    lines.extend(
        f"- {recommendation}"
        for recommendation in result["recommendations"] or ["No recommendations."]
    )
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check curated corpus health.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-quality", type=int, default=50)
    parser.add_argument("--min-high-quality-ratio", type=float, default=0.0)
    parser.add_argument("--max-missing-citation-ratio", type=float, default=0.2)
    parser.add_argument("--max-unreviewed-ratio", type=float, default=0.2)
    parser.add_argument("--max-duplicate-ids", type=int, default=0)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = check_corpus_health(
        input_path=args.input,
        strict=args.strict,
        min_quality=args.min_quality,
        min_high_quality_ratio=args.min_high_quality_ratio,
        max_missing_citation_ratio=args.max_missing_citation_ratio,
        max_unreviewed_ratio=args.max_unreviewed_ratio,
        max_duplicate_ids=args.max_duplicate_ids,
    )

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_health_report(result))

    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
