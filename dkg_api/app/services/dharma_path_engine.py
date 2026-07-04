from __future__ import annotations

from typing import Any


FOUNDATIONAL_PATH = [
    "impermanence",
    "suffering",
    "karma",
    "rebirth",
    "nirvana",
]

TRADITION_EXTENSIONS = {
    "theravada": ["cessation", "eightfold_path"],
    "mahayana": ["emptiness", "bodhisattva_path"],
    "vajrayana": ["bardo", "transformation"],
}


class DharmaPathEngine:
    def generate_path(
        self,
        user_profile: dict[str, Any],
        learning_state: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        learning_state = learning_state or {}
        path = list(FOUNDATIONAL_PATH)
        path.extend(self._tradition_extensions(user_profile))

        if user_profile.get("knowledge_level") == "beginner":
            path = path[:5]

        recommended_next = self._next_unmastered(path, learning_state)
        return {
            "user_id": user_profile.get("user_id"),
            "ordered_concepts": path,
            "recommended_next": recommended_next,
            "tradition_lens": user_profile.get("tradition_preference", []),
            "prerequisites_respected": True,
            "safety_note": "Tracks epistemic understanding, not spiritual attainment.",
        }

    def _tradition_extensions(self, user_profile: dict[str, Any]) -> list[str]:
        extensions = []
        for tradition in user_profile.get("tradition_preference") or []:
            for concept in TRADITION_EXTENSIONS.get(tradition, []):
                if concept not in extensions:
                    extensions.append(concept)
        return extensions

    def _next_unmastered(
        self,
        path: list[str],
        learning_state: dict[str, Any],
    ) -> str | None:
        mastered = set(learning_state.get("mastered_nodes") or [])
        confused = learning_state.get("confused_nodes") or []
        for concept in confused:
            if concept in path and concept not in mastered:
                return concept
        for concept in path:
            if concept not in mastered:
                return concept
        return None
