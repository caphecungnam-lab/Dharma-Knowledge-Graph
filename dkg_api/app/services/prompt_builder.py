from __future__ import annotations

from typing import Any

from dkg_api.app.core.truth_policy import ANTI_HALLUCINATION_RULES, tone_for_confidence


class PromptBuilder:
    def build(
        self,
        query: str,
        validated_context: list[dict[str, Any]],
        confidence: float,
    ) -> dict[str, object]:
        tone = self._tone(validated_context, confidence)
        return {
            "query": query,
            "tone": tone,
            "rules": ANTI_HALLUCINATION_RULES,
            "context": validated_context,
        }

    def _tone(
        self,
        validated_context: list[dict[str, Any]],
        confidence: float,
    ) -> str:
        epistemic_types = {
            str(context.get("epistemic_type") or "unknown")
            for context in validated_context
        }
        if epistemic_types & {
            "interpretive",
            "interpretive_view",
            "esoteric",
            "esoteric_view",
        }:
            return "interpretive"
        return tone_for_confidence(confidence)
