from __future__ import annotations

import re
from typing import Any

from dkg_api.app.safety.safety_policy import EPISTEMIC_LAYERS, SafetyPolicy


class OutputValidator:
    def __init__(self) -> None:
        self.policy = SafetyPolicy()

    def validate(
        self,
        answer: dict[str, Any] | str,
        context: list[dict[str, Any]],
    ) -> dict[str, object]:
        if isinstance(answer, str):
            answer_payload = {"answer": answer}
        else:
            answer_payload = answer

        errors = self._errors(answer_payload, context)
        return {
            "status": "APPROVED" if not errors else "REJECTED",
            "errors": errors,
        }

    def _errors(
        self,
        answer: dict[str, Any],
        context: list[dict[str, Any]],
    ) -> list[str]:
        errors = []
        context_node_ids = {str(node.get("node_id") or "") for node in context}
        context_sources = self._context_sources(context)
        used_nodes = {str(node_id) for node_id in answer.get("used_nodes", [])}
        confidence = float(answer.get("confidence") or 0.0)

        if not context:
            errors.append("missing_context")
        if not used_nodes or not used_nodes.issubset(context_node_ids):
            errors.append("missing_node_id_references")
        if not context_sources:
            errors.append("missing_source_id_references")
        if any(node.get("epistemic_type") not in EPISTEMIC_LAYERS for node in context):
            errors.append("missing_epistemic_type_tags")
        if self._merges_traditions(answer.get("answer", ""), context):
            errors.append("incorrect_tradition_merge")
        if self.policy.apply_tone_rules(confidence) == "refuse":
            errors.append("confidence_requires_refusal")
        if self._contains_untraceable_claim(answer.get("answer", ""), context):
            errors.append("untraceable_claim")
        return errors

    def _context_sources(self, context: list[dict[str, Any]]) -> set[str]:
        sources = set()
        for node in context:
            traceability = node.get("traceability") or {}
            for source in traceability.get("sources") or []:
                sources.add(str(source))
        return sources

    def _merges_traditions(self, answer: str, context: list[dict[str, Any]]) -> bool:
        traditions = {
            str(node.get("tradition") or "").lower()
            for node in context
            if node.get("tradition")
        }
        has_conflict = any(
            (node.get("conflict") or {}).get("type") not in {None, "", "none"}
            for node in context
        )
        merger_language = "all traditions agree" in answer.lower()
        return len(traditions) > 1 and has_conflict and merger_language

    def _contains_untraceable_claim(
        self,
        answer: str,
        context: list[dict[str, Any]],
    ) -> bool:
        sentences = [
            sentence.strip()
            for sentence in re.split(r"(?<=[.!?])\\s+", answer)
            if sentence.strip()
        ]
        if not sentences:
            return True

        context_text = " ".join(
            str((node.get("match") or {}).get("text") or "") for node in context
        ).lower()
        for sentence in sentences:
            normalized = self._remove_approved_prefix(sentence.lower().strip())
            if normalized and normalized not in context_text:
                return True
        return False

    def _remove_approved_prefix(self, sentence: str) -> str:
        if sentence.startswith("the validated context suggests:"):
            return sentence.split(":", 1)[-1].strip()
        if sentence.startswith("within the traceable esoteric context,"):
            return sentence.split(",", 1)[-1].strip()
        if sentence.startswith("in ") and "," in sentence:
            return sentence.split(",", 1)[-1].strip()
        return sentence
