from __future__ import annotations

from dkg_api.app.safety.safety_policy import (
    COMPARATIVE_TERMS,
    CORE_FACT_TERMS,
    ESOTERIC_TERMS,
    UNKNOWN_QUERY_TERMS,
    SafetyPolicy,
)


class EpistemicGateway:
    def __init__(self) -> None:
        self.policy = SafetyPolicy()

    def classify_query(self, query: str) -> dict[str, object]:
        normalized = query.lower().strip()
        if not normalized or self._contains_any(normalized, UNKNOWN_QUERY_TERMS):
            return {
                "mode": "reject",
                "allowed_layers": [],
                "risk_level": "high",
            }

        if self._contains_any(normalized, ESOTERIC_TERMS):
            mode = "esoteric"
            risk_level = "high"
        elif self._contains_any(normalized, COMPARATIVE_TERMS):
            mode = "multi_tradition"
            risk_level = "medium"
        elif self._contains_any(normalized, CORE_FACT_TERMS):
            mode = "core_fact"
            risk_level = "low"
        else:
            mode = "reject"
            risk_level = "high"

        return {
            "mode": mode,
            "allowed_layers": self.policy.allowed_layers_for_mode(mode),
            "risk_level": risk_level,
        }

    def _contains_any(self, text: str, terms: set[str]) -> bool:
        return any(term in text for term in terms)
