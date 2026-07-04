from __future__ import annotations

MIN_CONFIDENCE = 0.5

STABILITY_LOW_MAX = 0.7
STABILITY_MEDIUM_MAX = 0.9

ANTI_HALLUCINATION_RULES = [
    "Never introduce Buddhist doctrine that is not present in validated context.",
    "Never combine traditions unless they are explicitly present in validated context.",
    "Never answer when context is insufficient.",
    "Always reflect confidence level in tone.",
]


def stability_for_confidence(confidence: float) -> str:
    if confidence < STABILITY_LOW_MAX:
        return "low"
    if confidence < STABILITY_MEDIUM_MAX:
        return "medium"
    return "high"


def tone_for_confidence(confidence: float) -> str:
    if confidence >= 0.9:
        return "assertive"
    if confidence >= 0.7:
        return "academic"
    if confidence >= 0.5:
        return "interpretive"
    return "insufficient"
