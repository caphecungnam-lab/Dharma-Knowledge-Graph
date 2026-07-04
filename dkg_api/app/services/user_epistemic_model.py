from __future__ import annotations

from copy import deepcopy
from typing import Any


DEFAULT_CONCEPT_FAMILIARITY = {
    "impermanence": 0.2,
    "suffering": 0.1,
    "karma": 0.0,
    "rebirth": 0.0,
    "nirvana": 0.0,
    "emptiness": 0.0,
    "bardo": 0.0,
}


class UserEpistemicModel:
    def profile_user(self, user_id: str) -> dict[str, Any]:
        knowledge_level = self._knowledge_level(user_id)
        profile = {
            "user_id": user_id,
            "knowledge_level": knowledge_level,
            "tradition_preference": self._tradition_preference(user_id),
            "concept_familiarity": deepcopy(DEFAULT_CONCEPT_FAMILIARITY),
            "learning_style": self._learning_style(user_id),
            "epistemic_depth": self._epistemic_depth(knowledge_level),
            "tracking_scope": "epistemic_understanding_only",
        }
        return profile

    def _knowledge_level(self, user_id: str) -> str:
        normalized = user_id.lower()
        if "advanced" in normalized or "expert" in normalized:
            return "advanced"
        if "intermediate" in normalized:
            return "intermediate"
        return "beginner"

    def _tradition_preference(self, user_id: str) -> list[str]:
        normalized = user_id.lower()
        if "vajrayana" in normalized:
            return ["vajrayana"]
        if "mahayana" in normalized:
            return ["mahayana"]
        if "theravada" in normalized:
            return ["theravada"]
        return ["theravada", "mahayana", "vajrayana"]

    def _learning_style(self, user_id: str) -> str:
        normalized = user_id.lower()
        if "analytical" in normalized:
            return "analytical"
        if "contemplative" in normalized:
            return "contemplative"
        return "conceptual"

    def _epistemic_depth(self, knowledge_level: str) -> float:
        if knowledge_level == "advanced":
            return 0.8
        if knowledge_level == "intermediate":
            return 0.5
        return 0.2
