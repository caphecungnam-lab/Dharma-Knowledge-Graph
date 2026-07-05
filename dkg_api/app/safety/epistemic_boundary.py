from __future__ import annotations

from typing import Any

from dkg_api.app.safety.safety_policy import (
    critical_safety_failure,
    normalize_epistemic_type,
    normalize_tradition,
)


class EpistemicBoundary:
    def validate_transition(
        self,
        previous_type: object,
        next_type: object,
        *,
        validated: bool = False,
    ) -> dict[str, object]:
        previous = normalize_epistemic_type(previous_type)
        current = normalize_epistemic_type(next_type)
        if previous == current:
            return {"status": "ok"}
        if not validated:
            return critical_safety_failure(
                "epistemic_boundary",
                "epistemic_type_changed_without_validation",
            )
        if previous == "core_fact" and current in {"interpretive", "interpretive_view"}:
            return critical_safety_failure(
                "epistemic_boundary",
                "core_fact_cannot_be_overwritten_by_interpretive_view",
            )
        return {"status": "ok"}

    def enforce(self, context: list[dict[str, Any]]) -> dict[str, object]:
        filtered = []
        for node in context:
            transition = self._transition_for_node(node)
            if transition["status"] != "ok":
                return transition
            if self._is_invalid_cross_tradition_merge(node):
                return critical_safety_failure(
                    "epistemic_boundary",
                    "cross_tradition_merge_attempt",
                )
            filtered.append(node)
        return {"status": "ok", "context": self._isolate_esoteric(filtered)}

    def validate_answer(
        self,
        answer: dict[str, Any],
        context: list[dict[str, Any]],
    ) -> dict[str, object]:
        answer_text = str(answer.get("answer") or "").lower()
        context_traditions = {
            normalize_tradition(node.get("tradition"))
            for node in context
            if normalize_tradition(node.get("tradition"))
        }
        has_conflict = any(
            (node.get("conflict") or {}).get("type") not in {None, "", "none"}
            for node in context
        )
        if len(context_traditions) > 1 and has_conflict:
            merge_phrases = [
                "all traditions agree",
                "all buddhist traditions say the same",
                "there is no difference between traditions",
            ]
            if any(phrase in answer_text for phrase in merge_phrases):
                return critical_safety_failure(
                    "epistemic_boundary",
                    "doctrinal_differences_must_not_be_merged",
                )
        return {"status": "ok"}

    def _transition_for_node(self, node: dict[str, Any]) -> dict[str, object]:
        previous = node.get("previous_epistemic_type")
        current = node.get("epistemic_type")
        if previous is None:
            return {"status": "ok"}
        return self.validate_transition(
            previous,
            current,
            validated=bool(node.get("boundary_validated")),
        )

    def _is_invalid_cross_tradition_merge(self, node: dict[str, Any]) -> bool:
        if not node.get("merge_attempt"):
            return False
        traditions = node.get("merged_traditions") or []
        return len({str(item).lower() for item in traditions}) > 1

    def _isolate_esoteric(self, context: list[dict[str, Any]]) -> list[dict[str, Any]]:
        esoteric_nodes = [
            node
            for node in context
            if normalize_epistemic_type(node.get("epistemic_type")) == "esoteric"
        ]
        if esoteric_nodes:
            return esoteric_nodes
        return context
