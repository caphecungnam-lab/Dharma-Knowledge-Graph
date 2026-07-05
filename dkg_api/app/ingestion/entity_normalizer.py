from __future__ import annotations

from copy import deepcopy
from typing import Any

SYNONYMS = {
    "anicca": "impermanence",
    "vô thường": "impermanence",
    "dukkha": "suffering",
    "khổ": "suffering",
    "anatta": "non-self",
    "vô ngã": "non-self",
    "nibbana": "nirvana",
    "niết bàn": "nirvana",
    "sunyata": "emptiness",
    "śūnyatā": "emptiness",
    "tánh không": "emptiness",
}


class EntityNormalizer:
    def normalize(self, extracted: dict[str, list[dict[str, Any]]]) -> dict[str, list[dict[str, Any]]]:
        normalized = deepcopy(extracted)
        normalized["concepts"] = [
            self._normalize_concept(concept) for concept in extracted.get("concepts", [])
        ]
        normalized["relations"] = [
            self._normalize_relation(relation) for relation in extracted.get("relations", [])
        ]
        return normalized

    def _normalize_concept(self, concept: dict[str, Any]) -> dict[str, Any]:
        normalized = dict(concept)
        label = str(concept.get("label") or "").lower().strip()
        canonical = SYNONYMS.get(label, label)
        normalized["label"] = canonical
        normalized["id"] = f"concept_{canonical.replace(' ', '_').replace('-', '_')}"
        normalized["aliases"] = sorted(set([label, canonical]))
        return normalized

    def _normalize_relation(self, relation: dict[str, Any]) -> dict[str, Any]:
        normalized = dict(relation)
        for key in ("from", "to"):
            value = str(relation.get(key) or "").lower().strip()
            normalized[key] = SYNONYMS.get(value, value)
        return normalized
