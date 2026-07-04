from __future__ import annotations

from typing import Any


class ProgressionMapper:
    def map_progress(
        self,
        user_profile: dict[str, Any],
        learning_state: dict[str, Any],
    ) -> dict[str, Any]:
        nodes = []
        all_nodes = self._ordered_nodes(learning_state)
        for node_id in all_nodes:
            nodes.append(
                {
                    "node_id": node_id,
                    "state": self._state_for_node(node_id, learning_state),
                }
            )

        return {
            "user_id": user_profile.get("user_id"),
            "epistemic_depth": user_profile.get("epistemic_depth", 0.0),
            "states": [
                "ignorance",
                "exposure",
                "understanding",
                "integration",
                "realization",
            ],
            "state_note": "Realization means conceptual integration only, not spiritual attainment.",
            "nodes": nodes,
        }

    def _ordered_nodes(self, learning_state: dict[str, Any]) -> list[str]:
        ordered = []
        for bucket in ("seen_nodes", "mastered_nodes", "confused_nodes"):
            for node_id in learning_state.get(bucket) or []:
                if node_id not in ordered:
                    ordered.append(node_id)
        return ordered

    def _state_for_node(self, node_id: str, learning_state: dict[str, Any]) -> str:
        if node_id in set(learning_state.get("mastered_nodes") or []):
            return "integration"
        if node_id in set(learning_state.get("confused_nodes") or []):
            return "exposure"
        if node_id in set(learning_state.get("seen_nodes") or []):
            return "understanding"
        return "ignorance"
