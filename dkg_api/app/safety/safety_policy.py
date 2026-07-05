from __future__ import annotations


INSUFFICIENT_EPISTEMIC_DATA = "Insufficient epistemic data in DKG."
EPISTEMIC_SAFETY_VIOLATION = "epistemic_safety_violation"

CORE_FACT_TERMS = {
    "dukkha",
    "suffering",
    "impermanence",
    "karma",
    "rebirth",
    "nirvana",
    "emptiness",
    "death",
    "cái chết",
    "chet",
}

COMPARATIVE_TERMS = {
    "compare",
    "comparison",
    "tradition",
    "traditions",
    "theravada",
    "mahayana",
    "vajrayana",
}

ESOTERIC_TERMS = {
    "vajrayana",
    "tantra",
    "tantric",
    "esoteric",
    "bardo",
    "kim cương thừa",
    "kim cuong thua",
    "mật tông",
    "mat tong",
}

UNKNOWN_QUERY_TERMS = {
    "invent",
    "guess",
    "make up",
    "unverified",
}

EPISTEMIC_LAYERS = {
    "core_fact",
    "doctrinal",
    "doctrinal_view",
    "interpretive",
    "interpretive_view",
    "esoteric",
    "esoteric_view",
}

EPISTEMIC_TYPE_ALIASES = {
    "core_fact": "core_fact",
    "doctrinal": "doctrinal",
    "doctrinal_view": "doctrinal",
    "interpretive": "interpretive",
    "interpretive_view": "interpretive",
    "esoteric": "esoteric",
    "esoteric_view": "esoteric",
    "unknown": "unknown",
}

VALID_TRADITIONS = {
    "theravada",
    "mahayana",
    "vajrayana",
    "mixed",
}

TRADITION_ALIASES = {
    "shared_core": "mixed",
    "shared core": "mixed",
    "multi": "mixed",
}


def normalize_epistemic_type(value: object) -> str:
    normalized = str(value or "unknown").lower().strip()
    return EPISTEMIC_TYPE_ALIASES.get(normalized, "unknown")


def normalize_tradition(value: object) -> str | None:
    normalized = str(value or "").lower().strip()
    normalized = TRADITION_ALIASES.get(normalized, normalized)
    if normalized in VALID_TRADITIONS:
        return normalized
    return None


def rejected_response(
    missing: list[str],
    safety: dict[str, object] | None = None,
) -> dict[str, object]:
    response: dict[str, object] = {
        "status": "rejected",
        "reason": EPISTEMIC_SAFETY_VIOLATION,
        "missing": missing,
    }
    if safety is not None:
        response["safety"] = safety
    return response


def critical_safety_failure(layer: str, reason: str) -> dict[str, object]:
    return {
        "status": "critical_safety_failure",
        "layer": layer,
        "reason": reason,
    }


class SafetyPolicy:
    def apply_tone_rules(self, confidence: float) -> str:
        if confidence >= 0.9:
            return "assertive"
        if 0.7 <= confidence < 0.9:
            return "academic"
        if 0.5 <= confidence < 0.7:
            return "interpretive"
        return "refuse"

    def allowed_layers_for_mode(self, mode: str) -> list[str]:
        if mode == "core_fact":
            return ["core_fact", "doctrinal"]
        if mode == "multi_tradition":
            return ["core_fact", "doctrinal", "interpretive"]
        if mode == "esoteric":
            return ["esoteric"]
        return []
