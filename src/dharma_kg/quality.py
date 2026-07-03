"""Evidence quality scoring helpers."""

from __future__ import annotations

from typing import Any

from dharma_kg.citations import build_youtube_timestamp_url

MAX_QUALITY_SCORE = 100


def has_evidence_text(node: dict[str, Any]) -> bool:
    return len(str(node.get("evidence_text", "")).strip()) >= 20


def has_field(node: dict[str, Any], field: str) -> bool:
    return bool(str(node.get(field, "")).strip())


def has_citation_url(node: dict[str, Any]) -> bool:
    if has_field(node, "citation_url"):
        return True
    return (
        build_youtube_timestamp_url(
            str(node.get("source_url", "")),
            str(node.get("start_time", "")),
        )
        is not None
    )


def get_quality_flags(node: dict[str, Any]) -> list[str]:
    flags: list[str] = []

    if has_evidence_text(node):
        flags.append("has_text")
    if has_field(node, "start_time"):
        flags.append("has_start_time")
    if has_field(node, "end_time"):
        flags.append("has_end_time")
    if has_field(node, "source_url"):
        flags.append("has_source_url")
    if has_citation_url(node):
        flags.append("has_citation_url")
    if node.get("review_status") == "human_reviewed":
        flags.append("human_reviewed")
    if node.get("review_status") == "verified":
        flags.append("verified")
    if node.get("curated_status") == "curated":
        flags.append("curated")
    if has_field(node, "speaker"):
        flags.append("has_speaker")
    if has_field(node, "evidence_type"):
        flags.append("has_evidence_type")
    if has_field(node, "confidence"):
        flags.append("has_confidence")

    return flags


def score_evidence(node: dict[str, Any]) -> dict[str, Any]:
    score = 0

    if has_evidence_text(node):
        score += 20
    if has_field(node, "start_time"):
        score += 10
    if has_field(node, "end_time"):
        score += 10
    if has_field(node, "source_url"):
        score += 10
    if has_citation_url(node):
        score += 10
    if node.get("review_status") == "human_reviewed":
        score += 15
    if node.get("review_status") == "verified":
        score += 20
    if node.get("curated_status") == "curated":
        score += 10
    if has_field(node, "speaker"):
        score += 5
    if has_field(node, "evidence_type"):
        score += 5
    if has_field(node, "confidence"):
        score += 5

    return {
        "quality_score": min(score, MAX_QUALITY_SCORE),
        "quality_flags": get_quality_flags(node),
    }
