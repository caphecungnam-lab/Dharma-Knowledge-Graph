from __future__ import annotations

from collections import defaultdict
from typing import Any

from dkg_api.app.ingestion.entity_normalizer import SYNONYMS


class DeduplicationEngine:
    def analyze(self, concepts: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        by_canonical: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for concept in concepts:
            label = str(concept.get("label") or concept.get("canonical_label") or "").lower().strip()
            canonical = SYNONYMS.get(label, label)
            by_canonical[canonical].append(concept)

        duplicates = []
        conflicts = []
        for canonical, group in by_canonical.items():
            labels = {
                str(concept.get("label") or "").lower().strip()
                for concept in group
            }
            definitions = {
                self._normalize_definition(concept.get("definition"))
                for concept in group
                if concept.get("definition")
            }
            traditions = {
                str(concept.get("tradition") or "").lower().strip()
                for concept in group
                if concept.get("tradition")
            }
            if len(group) > 1 and len(labels) > 1:
                duplicates.append(
                    {
                        "canonical": canonical,
                        "labels": sorted(labels),
                        "count": len(group),
                    }
                )
            if len(definitions) > 1:
                conflicts.append(
                    {
                        "canonical": canonical,
                        "type": "conflicting_definitions",
                        "traditions": sorted(traditions),
                    }
                )

        return {
            "duplicates": duplicates,
            "conflicts": conflicts,
            "merged_suggestions": [
                {
                    "canonical": duplicate["canonical"],
                    "labels": duplicate["labels"],
                    "action": "review_only_no_auto_merge",
                }
                for duplicate in duplicates
            ],
        }

    def _normalize_definition(self, value: object) -> str:
        return " ".join(str(value or "").lower().split())
