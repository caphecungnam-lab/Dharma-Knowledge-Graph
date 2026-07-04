from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any


EMPTY_STATE = {
    "seen_nodes": [],
    "mastered_nodes": [],
    "confused_nodes": [],
    "recommended_review": [],
}


class LearningStateTracker:
    def __init__(self) -> None:
        self._states: dict[str, dict[str, Any]] = {}

    def state_for(self, user_id: str) -> dict[str, Any]:
        state = deepcopy(self._states.get(user_id) or EMPTY_STATE)
        state["user_id"] = user_id
        state["tracking_scope"] = "epistemic_understanding_only"
        return state

    def update_state(
        self,
        user_id: str,
        seen_nodes: list[str] | None = None,
        mastered_nodes: list[str] | None = None,
        confused_nodes: list[str] | None = None,
    ) -> dict[str, Any]:
        state = self.state_for(user_id)
        state["seen_nodes"] = self._merge(state["seen_nodes"], seen_nodes or [])
        state["mastered_nodes"] = self._merge(
            state["mastered_nodes"], mastered_nodes or []
        )
        state["confused_nodes"] = self._merge(
            state["confused_nodes"], confused_nodes or []
        )
        state["recommended_review"] = self._recommended_review(state)
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        self._states[user_id] = deepcopy(state)
        return state

    def _merge(self, existing: list[str], incoming: list[str]) -> list[str]:
        merged = list(existing)
        for value in incoming:
            if value and value not in merged:
                merged.append(value)
        return merged

    def _recommended_review(self, state: dict[str, Any]) -> list[str]:
        mastered = set(state.get("mastered_nodes") or [])
        review = []
        for node_id in state.get("confused_nodes") or []:
            if node_id not in mastered and node_id not in review:
                review.append(node_id)
        return review
