from __future__ import annotations

from typing import Any

EPISTEMIC_TYPES = {
    "core_fact",
    "doctrinal_view",
    "interpretive_view",
    "esoteric_view",
    "unknown",
}


def classify_epistemic_type(node: dict[str, Any]) -> str:
    match = node.get("match", {})
    related = node.get("related", [])
    source_type = str(match.get("source_type") or "").lower()
    tradition = str(match.get("tradition") or "").lower()
    text = str(match.get("text") or "").lower()
    source_id = str(match.get("source_id") or "")

    if not source_id and not source_type:
        return "unknown"

    if source_type == "sutta":
        return "core_fact"

    if _is_esoteric(tradition, text):
        return "esoteric_view"

    traditions = _traditions(match, related)
    if len(traditions) > 1:
        if _has_interpretive_difference(related):
            return "interpretive_view"
        return "doctrinal_view"

    if tradition:
        return "doctrinal_view"

    return "unknown"


def _is_esoteric(tradition: str, text: str) -> bool:
    return (
        "vajrayana" in tradition
        or "tantra" in text
        or "tantric" in text
        or "esoteric" in text
    )


def _traditions(match: dict[str, Any], related: list[dict[str, Any]]) -> set[str]:
    traditions = {str(match.get("tradition") or "").lower().strip()}
    for node in related:
        traditions.add(str(node.get("tradition") or "").lower().strip())
    return {tradition for tradition in traditions if tradition}


def _has_interpretive_difference(related: list[dict[str, Any]]) -> bool:
    markers = {"interpretation", "view", "differs", "commentary"}
    for node in related:
        text = " ".join(
            [
                str(node.get("label") or ""),
                str(node.get("definition") or ""),
            ]
        ).lower()
        if any(marker in text for marker in markers):
            return True
    return False
