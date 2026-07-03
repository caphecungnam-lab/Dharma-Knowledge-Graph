#!/usr/bin/env python3
"""Build a corpus dashboard report from the curated Evidence index."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dharma_kg.quality import score_evidence  # noqa: E402

DEFAULT_INPUT_PATH = (
    Path("data") / "indexes" / "giac_khang" / "curated_evidence_index.json"
)
DEFAULT_OUTPUT_MD = Path("reports") / "giac_khang" / "corpus_dashboard.md"
DEFAULT_OUTPUT_JSON = Path("reports") / "giac_khang" / "corpus_dashboard.json"
DASHBOARD_NAME = "giac_khang_corpus_dashboard"


def current_local_iso_datetime() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def is_evidence_node(node: Any) -> bool:
    return isinstance(node, dict) and node.get("type") == "Evidence"


def evidence_nodes(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [node for node in payload.get("nodes", []) if is_evidence_node(node)]


def has_value(node: dict[str, Any], field: str) -> bool:
    return bool(str(node.get(field, "")).strip())


def quality_score(node: dict[str, Any]) -> int:
    if node.get("quality_score") is not None:
        return int(node.get("quality_score", 0))
    return int(score_evidence(node)["quality_score"])


def quality_flags(node: dict[str, Any]) -> list[str]:
    flags = node.get("quality_flags")
    if isinstance(flags, list):
        return [str(flag) for flag in flags]
    return [str(flag) for flag in score_evidence(node)["quality_flags"]]


def evidence_text(node: dict[str, Any]) -> str:
    return str(node.get("evidence_text", ""))


def short_text(value: str, limit: int = 96) -> str:
    cleaned = " ".join(str(value).split())
    if len(cleaned) <= limit:
        return cleaned
    return f"{cleaned[: limit - 1]}..."


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|")


def sorted_counter(counter: Counter[str]) -> dict[str, int]:
    return {key: counter[key] for key in sorted(counter)}


def missing_flags(node: dict[str, Any]) -> list[str]:
    checks = {
        "missing_evidence_text": has_value(node, "evidence_text"),
        "missing_start_time": has_value(node, "start_time"),
        "missing_end_time": has_value(node, "end_time"),
        "missing_source_url": has_value(node, "source_url"),
        "missing_citation_url": has_value(node, "citation_url"),
        "missing_speaker": has_value(node, "speaker"),
        "missing_evidence_type": has_value(node, "evidence_type"),
        "missing_confidence": has_value(node, "confidence"),
    }
    return [name for name, present in checks.items() if not present]


def evidence_summary(node: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": node.get("id", ""),
        "quality_score": quality_score(node),
        "start_time": node.get("start_time", ""),
        "end_time": node.get("end_time", ""),
        "evidence_text": short_text(evidence_text(node)),
        "missing_flags": missing_flags(node),
    }


def count_by_field(nodes: list[dict[str, Any]], field: str) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for node in nodes:
        value = str(node.get(field, "")).strip() or "(missing)"
        counter[value] += 1
    return sorted_counter(counter)


def score_values(nodes: list[dict[str, Any]]) -> list[int]:
    return [quality_score(node) for node in nodes]


def top_low_quality(
    nodes: list[dict[str, Any]], limit: int = 10
) -> list[dict[str, Any]]:
    return [
        evidence_summary(node)
        for node in sorted(
            nodes,
            key=lambda node: (
                quality_score(node),
                str(node.get("start_time", "")),
                str(node.get("id", "")),
            ),
        )[:limit]
    ]


def top_missing_citation_url(
    nodes: list[dict[str, Any]], limit: int = 10
) -> list[dict[str, Any]]:
    missing = [node for node in nodes if not has_value(node, "citation_url")]
    return [
        evidence_summary(node)
        for node in sorted(
            missing,
            key=lambda node: (
                quality_score(node),
                str(node.get("start_time", "")),
                str(node.get("id", "")),
            ),
        )[:limit]
    ]


def top_by_text_length(
    nodes: list[dict[str, Any]],
    reverse: bool,
    limit: int = 10,
) -> list[dict[str, Any]]:
    return [
        evidence_summary(node)
        for node in sorted(
            nodes,
            key=lambda node: (
                len(evidence_text(node)),
                str(node.get("start_time", "")),
                str(node.get("id", "")),
            ),
            reverse=reverse,
        )[:limit]
    ]


def build_recommendations(metrics: dict[str, Any]) -> list[str]:
    recommendations: list[str] = []
    total_evidence = metrics["core"]["total_evidence"]

    if metrics["citation"]["missing_citation_url_count"] > 0:
        recommendations.append("Rebuild the curated index after DKG-014.")
    if metrics["quality"]["needs_review_count"] > 0:
        recommendations.append(
            "Use batch_review_helper to review low-quality Evidence."
        )
    if metrics["core"]["human_reviewed_count"] < total_evidence:
        recommendations.append("Review remaining Evidence before promotion.")
    if total_evidence < 50:
        recommendations.append("Continue batch ingestion to expand corpus coverage.")

    return recommendations


def build_dashboard(
    payload: dict[str, Any],
    input_path: Path,
    min_high_quality: int = 80,
    min_needs_review: int = 50,
    generated_at: str | None = None,
) -> dict[str, Any]:
    nodes = evidence_nodes(payload)
    scores = score_values(nodes)
    total = len(nodes)

    core = {
        "total_evidence": total,
        "curated_count": sum(
            1 for node in nodes if node.get("curated_status") == "curated"
        ),
        "human_reviewed_count": sum(
            1 for node in nodes if node.get("review_status") == "human_reviewed"
        ),
        "verified_count": sum(
            1 for node in nodes if node.get("review_status") == "verified"
        ),
        "rejected_count": sum(
            1 for node in nodes if node.get("review_status") == "rejected"
        ),
        "unreviewed_count": sum(
            1 for node in nodes if node.get("review_status") == "unreviewed"
        ),
    }
    citation = {
        "has_source_url_count": sum(
            1 for node in nodes if has_value(node, "source_url")
        ),
        "has_citation_url_count": sum(
            1 for node in nodes if has_value(node, "citation_url")
        ),
        "missing_source_url_count": sum(
            1 for node in nodes if not has_value(node, "source_url")
        ),
        "missing_timestamp_count": sum(
            1 for node in nodes if not has_value(node, "start_time")
        ),
        "missing_citation_url_count": sum(
            1 for node in nodes if not has_value(node, "citation_url")
        ),
    }
    high_quality_count = sum(1 for score in scores if score >= min_high_quality)
    needs_review_count = sum(1 for score in scores if score < min_needs_review)
    medium_quality_count = total - high_quality_count - needs_review_count
    quality = {
        "average_quality_score": round(sum(scores) / total, 2) if total else 0,
        "min_quality_score": min(scores) if scores else 0,
        "max_quality_score": max(scores) if scores else 0,
        "high_quality_count": high_quality_count,
        "medium_quality_count": medium_quality_count,
        "needs_review_count": needs_review_count,
    }
    metadata_gaps = {
        "missing_evidence_text_count": sum(
            1 for node in nodes if not has_value(node, "evidence_text")
        ),
        "missing_start_time_count": sum(
            1 for node in nodes if not has_value(node, "start_time")
        ),
        "missing_end_time_count": sum(
            1 for node in nodes if not has_value(node, "end_time")
        ),
        "missing_speaker_count": sum(
            1 for node in nodes if not has_value(node, "speaker")
        ),
        "missing_evidence_type_count": sum(
            1 for node in nodes if not has_value(node, "evidence_type")
        ),
        "missing_confidence_count": sum(
            1 for node in nodes if not has_value(node, "confidence")
        ),
    }
    source_coverage = {
        "evidence_by_source_url": count_by_field(nodes, "source_url"),
        "evidence_by_document_id": count_by_field(nodes, "document_id"),
        "evidence_by_speaker": count_by_field(nodes, "speaker"),
        "earliest_start_time": min(
            [
                str(node.get("start_time", ""))
                for node in nodes
                if has_value(node, "start_time")
            ],
            default="",
        ),
        "latest_end_time": max(
            [
                str(node.get("end_time", ""))
                for node in nodes
                if has_value(node, "end_time")
            ],
            default="",
        ),
    }
    metrics = {
        "core": core,
        "citation": citation,
        "quality": quality,
        "metadata_gaps": metadata_gaps,
        "source_coverage": source_coverage,
    }

    return {
        "metadata": {
            "dashboard_name": DASHBOARD_NAME,
            "generated_at": generated_at or current_local_iso_datetime(),
            "input": str(input_path),
        },
        "metrics": {
            **core,
            **citation,
            **quality,
            **metadata_gaps,
        },
        "quality_distribution": {
            f"high_quality_gte_{min_high_quality}": high_quality_count,
            f"medium_quality_{min_needs_review}_to_{min_high_quality - 1}": medium_quality_count,
            f"needs_review_lt_{min_needs_review}": needs_review_count,
        },
        "citation_readiness": citation,
        "metadata_gaps": metadata_gaps,
        "source_coverage": source_coverage,
        "top_low_quality_evidence": top_low_quality(nodes),
        "top_10_missing_citation_url": top_missing_citation_url(nodes),
        "top_10_longest_evidence_text": top_by_text_length(nodes, reverse=True),
        "top_10_shortest_evidence_text": top_by_text_length(nodes, reverse=False),
        "recommendations": build_recommendations(metrics),
    }


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| "
        + " | ".join("---" if index == 0 else "---:" for index, _ in enumerate(headers))
        + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(markdown_cell(value) for value in row) + " |")
    return "\n".join(lines)


def coverage_lines(title: str, values: dict[str, int]) -> list[str]:
    lines = [f"### {title}", ""]
    rows = [[key, count] for key, count in values.items()]
    lines.append(markdown_table(["Value", "Count"], rows or [["(none)", 0]]))
    return lines


def top_low_quality_markdown(items: list[dict[str, Any]]) -> str:
    rows = [
        [
            item["id"],
            item["quality_score"],
            item["start_time"],
            item["evidence_text"],
            ", ".join(item["missing_flags"]),
        ]
        for item in items
    ]
    return markdown_table(
        ["ID", "Quality", "Start", "Evidence Text", "Missing Flags"],
        rows or [["(none)", 0, "", "", ""]],
    )


def render_markdown_report(dashboard: dict[str, Any]) -> str:
    metrics = dashboard["metrics"]
    distribution = dashboard["quality_distribution"]
    citation = dashboard["citation_readiness"]
    gaps = dashboard["metadata_gaps"]
    coverage = dashboard["source_coverage"]

    lines = [
        "# Giác Khang Corpus Dashboard",
        "",
        f"Generated at: {dashboard['metadata']['generated_at']}",
        "",
        "## Summary",
        "",
        markdown_table(
            ["Metric", "Value"],
            [
                ["Total Evidence", metrics["total_evidence"]],
                ["Human reviewed", metrics["human_reviewed_count"]],
                ["Curated", metrics["curated_count"]],
                ["High quality Evidence", metrics["high_quality_count"]],
                ["Needs review", metrics["needs_review_count"]],
                ["Citation URL available", metrics["has_citation_url_count"]],
            ],
        ),
        "",
        "## Quality Distribution",
        "",
        markdown_table(
            ["Bucket", "Count"],
            [
                ["High quality >= 80", distribution["high_quality_gte_80"]],
                ["Medium 50-79", distribution["medium_quality_50_to_79"]],
                ["Needs review < 50", distribution["needs_review_lt_50"]],
            ],
        ),
        "",
        "## Citation Readiness",
        "",
        markdown_table(
            ["Metric", "Count"],
            [
                ["Has source URL", citation["has_source_url_count"]],
                ["Has citation URL", citation["has_citation_url_count"]],
                ["Missing citation URL", citation["missing_citation_url_count"]],
                ["Missing timestamp", citation["missing_timestamp_count"]],
            ],
        ),
        "",
        "## Metadata Gaps",
        "",
        markdown_table(
            ["Missing Field", "Count"],
            [
                ["evidence_text", gaps["missing_evidence_text_count"]],
                ["start_time", gaps["missing_start_time_count"]],
                ["end_time", gaps["missing_end_time_count"]],
                ["speaker", gaps["missing_speaker_count"]],
                ["evidence_type", gaps["missing_evidence_type_count"]],
                ["confidence", gaps["missing_confidence_count"]],
            ],
        ),
        "",
        "## Source Coverage",
        "",
        f"Earliest start time: {coverage['earliest_start_time'] or '(none)'}",
        "",
        f"Latest end time: {coverage['latest_end_time'] or '(none)'}",
        "",
        *coverage_lines("Source URL", coverage["evidence_by_source_url"]),
        "",
        *coverage_lines("Document ID", coverage["evidence_by_document_id"]),
        "",
        *coverage_lines("Speaker", coverage["evidence_by_speaker"]),
        "",
        "## Top Low Quality Evidence",
        "",
        top_low_quality_markdown(dashboard["top_low_quality_evidence"]),
        "",
        "## Recommendations",
        "",
    ]

    recommendations = dashboard["recommendations"] or ["No immediate recommendations."]
    lines.extend(f"- {recommendation}" for recommendation in recommendations)
    lines.append("")
    return "\n".join(lines)


def build_corpus_dashboard_file(
    input_path: Path = DEFAULT_INPUT_PATH,
    output_md: Path = DEFAULT_OUTPUT_MD,
    output_json: Path = DEFAULT_OUTPUT_JSON,
    min_high_quality: int = 80,
    min_needs_review: int = 50,
) -> dict[str, Any]:
    payload = load_json(input_path)
    dashboard = build_dashboard(
        payload,
        input_path=input_path,
        min_high_quality=min_high_quality,
        min_needs_review=min_needs_review,
    )
    write_json(output_json, dashboard)
    write_text(output_md, render_markdown_report(dashboard))
    return dashboard


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Giac Khang corpus dashboard.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--min-high-quality", type=int, default=80)
    parser.add_argument("--min-needs-review", type=int, default=50)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    dashboard = build_corpus_dashboard_file(
        input_path=args.input,
        output_md=args.output_md,
        output_json=args.output_json,
        min_high_quality=args.min_high_quality,
        min_needs_review=args.min_needs_review,
    )
    print(
        f"Wrote {args.output_md} and {args.output_json} "
        f"for {dashboard['metrics']['total_evidence']} Evidence node(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
