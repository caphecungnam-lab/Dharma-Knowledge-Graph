from __future__ import annotations


INSUFFICIENT_EPISTEMIC_DATA = "Insufficient epistemic data in DKG."

CORE_FACT_TERMS = {
    "dukkha",
    "suffering",
    "impermanence",
    "karma",
    "rebirth",
    "nirvana",
    "emptiness",
    "death",
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
}

UNKNOWN_QUERY_TERMS = {
    "invent",
    "guess",
    "make up",
    "unverified",
}

EPISTEMIC_LAYERS = {
    "core_fact",
    "doctrinal_view",
    "interpretive_view",
    "esoteric_view",
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
            return ["core_fact", "doctrinal_view"]
        if mode == "multi_tradition":
            return ["core_fact", "doctrinal_view", "interpretive_view"]
        if mode == "esoteric":
            return ["esoteric_view"]
        return []
