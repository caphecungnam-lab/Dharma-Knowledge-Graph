from __future__ import annotations

from typing import Any


class AdaptiveExplainer:
    def explain(
        self,
        concept: str,
        user_profile: dict[str, Any],
        context: list[dict[str, Any]],
    ) -> dict[str, Any]:
        usable_context = [
            item for item in context if item.get("ai_usage_allowed") is not False
        ]
        if not usable_context:
            return {
                "concept": concept,
                "explanation": "Insufficient verified data in Dharma Knowledge Graph.",
                "confidence": 0.0,
                "used_nodes": [],
                "tone": "refusal",
            }

        knowledge_level = str(user_profile.get("knowledge_level") or "beginner")
        confidence = self._average_confidence(usable_context)
        explanation = self._build_explanation(
            concept,
            knowledge_level,
            user_profile,
            usable_context,
        )
        return {
            "concept": concept,
            "explanation": explanation,
            "confidence": confidence,
            "used_nodes": [item.get("node_id") for item in usable_context],
            "tone": self._tone(knowledge_level, confidence),
            "tracking_scope": "epistemic_understanding_only",
        }

    def _build_explanation(
        self,
        concept: str,
        knowledge_level: str,
        user_profile: dict[str, Any],
        context: list[dict[str, Any]],
    ) -> str:
        label = self._label(concept, context)
        definitions = self._definitions(context)
        base = definitions[0] if definitions else label

        if knowledge_level == "beginner":
            return f"{label}: {base}"

        traditions = self._traditions(context)
        if knowledge_level == "intermediate":
            return (
                f"{label}: {base} "
                f"Context traditions: {', '.join(traditions) or 'unspecified'}."
            )

        conflicts = self._conflicts(context)
        esoteric = self._allowed_esoteric_context(user_profile, context)
        parts = [
            f"{label}: {base}",
            f"Epistemic types: {', '.join(self._epistemic_types(context))}.",
        ]
        if conflicts:
            parts.append(f"Conflicts present: {', '.join(conflicts)}.")
        if esoteric:
            parts.append("Vajrayana/esoteric framing is included only from validated context.")
        return " ".join(parts)

    def _average_confidence(self, context: list[dict[str, Any]]) -> float:
        values = [float(item.get("confidence") or 0.0) for item in context]
        return round(sum(values) / len(values), 3)

    def _tone(self, knowledge_level: str, confidence: float) -> str:
        if confidence < 0.5:
            return "insufficient"
        if knowledge_level == "advanced":
            return "epistemic-analytical"
        if knowledge_level == "intermediate":
            return "comparative-academic"
        return "simple-foundational"

    def _label(self, concept: str, context: list[dict[str, Any]]) -> str:
        match = context[0].get("match") or {}
        return str(match.get("label") or concept)

    def _definitions(self, context: list[dict[str, Any]]) -> list[str]:
        definitions = []
        for item in context:
            match = item.get("match") or {}
            text = str(match.get("definition") or match.get("text") or "").strip()
            if text and text not in definitions:
                definitions.append(text)
        return definitions

    def _traditions(self, context: list[dict[str, Any]]) -> list[str]:
        traditions = []
        for item in context:
            tradition = str(item.get("tradition") or "").strip()
            if tradition and tradition not in traditions:
                traditions.append(tradition)
        return traditions

    def _epistemic_types(self, context: list[dict[str, Any]]) -> list[str]:
        types = []
        for item in context:
            epistemic_type = str(item.get("epistemic_type") or "").strip()
            if epistemic_type and epistemic_type not in types:
                types.append(epistemic_type)
        return types

    def _conflicts(self, context: list[dict[str, Any]]) -> list[str]:
        conflicts = []
        for item in context:
            conflict = item.get("conflict") or {}
            conflict_type = str(conflict.get("type") or "").strip()
            if conflict_type and conflict_type != "none" and conflict_type not in conflicts:
                conflicts.append(conflict_type)
        return conflicts

    def _allowed_esoteric_context(
        self,
        user_profile: dict[str, Any],
        context: list[dict[str, Any]],
    ) -> bool:
        preferences = set(user_profile.get("tradition_preference") or [])
        if "vajrayana" not in preferences:
            return False
        return any(
            item.get("epistemic_type") == "esoteric_view"
            and item.get("ai_usage_allowed") is True
            for item in context
        )
