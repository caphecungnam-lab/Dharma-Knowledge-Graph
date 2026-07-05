from __future__ import annotations

from collections import Counter
from typing import Any

from dkg_api.app.services.prompt_builder import PromptBuilder

INSUFFICIENT_ANSWER = "Insufficient verified data in Dharma Knowledge Graph."


class AIReasoner:
    def __init__(self) -> None:
        self.prompt_builder = PromptBuilder()

    def generate(
        self,
        query: str,
        validated_context: list[dict[str, Any]],
    ) -> dict[str, object]:
        if not validated_context:
            return {
                "answer": INSUFFICIENT_ANSWER,
                "confidence": 0.0,
            }

        confidence = self._overall_confidence(validated_context)
        prompt = self.prompt_builder.build(query, validated_context, confidence)
        used_nodes = [context["node_id"] for context in validated_context]
        answer = self._build_answer(prompt, validated_context, confidence)

        return {
            "answer": answer,
            "confidence": confidence,
            "used_nodes": used_nodes,
            "used_sources": self._used_sources(validated_context),
            "epistemic_types": self._epistemic_types(validated_context),
            "sentence_node_map": self._sentence_node_map(answer, validated_context),
            "tradition_distribution": self._tradition_distribution(validated_context),
        }

    def _overall_confidence(self, contexts: list[dict[str, Any]]) -> float:
        if not contexts:
            return 0.0
        return round(
            sum(float(context["confidence"]) for context in contexts) / len(contexts),
            3,
        )

    def _build_answer(
        self,
        prompt: dict[str, object],
        contexts: list[dict[str, Any]],
        confidence: float,
    ) -> str:
        tone = str(prompt["tone"])
        statements = []
        for context in contexts:
            match = context.get("match", {})
            text = str(match.get("text") or "").strip()
            tradition = str(match.get("tradition") or "").strip()
            epistemic_type = str(context.get("epistemic_type") or "unknown")
            if not text:
                continue
            if tone == "assertive":
                statements.append(text)
            elif tone == "academic":
                prefix = f"In {tradition}, " if tradition else ""
                statements.append(f"{prefix}{text}")
            else:
                statements.append(f"The validated context suggests: {text}")
            if epistemic_type in {"esoteric", "esoteric_view"}:
                statements[-1] = f"Within the traceable esoteric context, {text}"

        if not statements or confidence < 0.5:
            return INSUFFICIENT_ANSWER

        return " ".join(statements)

    def _tradition_distribution(
        self,
        contexts: list[dict[str, Any]],
    ) -> dict[str, float]:
        base_traditions = ["theravada", "mahayana", "vajrayana"]
        traditions = [
            str(context.get("tradition") or "unknown") for context in contexts
        ]
        counts = Counter(traditions)
        total = sum(counts.values())
        if total == 0:
            return {tradition: 0.0 for tradition in base_traditions}
        return {
            tradition: round((counts.get(tradition, 0) / total) * 100, 1)
            for tradition in base_traditions
        }

    def _used_sources(self, contexts: list[dict[str, Any]]) -> list[str]:
        sources = []
        for context in contexts:
            traceability = context.get("traceability") or {}
            for source in traceability.get("sources") or []:
                text = str(source)
                if text and text not in sources:
                    sources.append(text)
        return sources

    def _epistemic_types(self, contexts: list[dict[str, Any]]) -> list[str]:
        epistemic_types = []
        for context in contexts:
            epistemic_type = str(context.get("epistemic_type") or "")
            if epistemic_type and epistemic_type not in epistemic_types:
                epistemic_types.append(epistemic_type)
        return epistemic_types

    def _sentence_node_map(
        self,
        answer: str,
        contexts: list[dict[str, Any]],
    ) -> dict[str, str]:
        sentences = [sentence.strip() for sentence in answer.split(".") if sentence.strip()]
        mapping: dict[str, str] = {}
        if not contexts:
            return mapping
        fallback_node_id = str(contexts[0].get("node_id") or "")
        for sentence in sentences:
            mapping[sentence] = self._best_node_for_sentence(sentence, contexts) or fallback_node_id
        return mapping

    def _best_node_for_sentence(
        self,
        sentence: str,
        contexts: list[dict[str, Any]],
    ) -> str | None:
        normalized_sentence = sentence.lower()
        for context in contexts:
            text = str((context.get("match") or {}).get("text") or "").lower()
            if text and text in normalized_sentence:
                return str(context.get("node_id") or "")
        return None
