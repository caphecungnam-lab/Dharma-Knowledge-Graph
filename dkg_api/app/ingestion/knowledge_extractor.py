from __future__ import annotations

import re
from typing import Any

CONCEPT_PATTERNS = {
    "impermanence": ["impermanence", "anicca", "vô thường"],
    "suffering": ["suffering", "dukkha", "khổ"],
    "non-self": ["non-self", "anatta", "vô ngã"],
    "karma": ["karma", "kamma", "nghiệp"],
    "rebirth": ["rebirth", "tái sinh"],
    "nirvana": ["nirvana", "nibbana", "niết bàn"],
    "death": ["death", "dying", "cái chết", "chết"],
    "bardo": ["bardo"],
    "emptiness": ["emptiness", "sunyata", "śūnyatā", "tánh không"],
}

RELATION_MARKERS = {
    "RELATED_TO": ["related to", "connected to", "liên hệ"],
    "CONTRASTS_WITH": ["contrasts with", "differs from", "khác với"],
    "MENTIONS": ["mentions", "states", "says", "nói"],
}


class KnowledgeExtractor:
    def extract(
        self,
        chunk: dict[str, Any],
        source_metadata: dict[str, Any] | None = None,
    ) -> dict[str, list[dict[str, Any]]]:
        metadata = source_metadata or {}
        text = str(chunk.get("text") or "")
        concepts = self._concepts(text, chunk, metadata)
        return {
            "concepts": concepts,
            "relations": self._relations(text, concepts),
            "statements": self._statements(text, concepts, chunk, metadata),
        }

    def _concepts(
        self,
        text: str,
        chunk: dict[str, Any],
        metadata: dict[str, Any],
    ) -> list[dict[str, Any]]:
        lowered = text.lower()
        concepts = []
        for label, variants in CONCEPT_PATTERNS.items():
            matched = [variant for variant in variants if variant in lowered]
            if not matched:
                continue
            concepts.append(
                {
                    "id": f"concept_{label.replace(' ', '_').replace('-', '_')}",
                    "label": matched[0],
                    "canonical_label": label,
                    "definition": text,
                    "source_id": metadata.get("source_id"),
                    "source_type": metadata.get("source_type", "text"),
                    "tradition": metadata.get("tradition", "unknown"),
                    "chunk_id": chunk.get("chunk_id"),
                    "position": chunk.get("position"),
                }
            )
        return concepts

    def _relations(
        self,
        text: str,
        concepts: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        if len(concepts) < 2:
            return []
        relation_type = self._relation_type(text)
        relations = []
        for index, source in enumerate(concepts):
            for target in concepts[index + 1 :]:
                relations.append(
                    {
                        "from": source["canonical_label"],
                        "to": target["canonical_label"],
                        "type": relation_type,
                    }
                )
        return relations

    def _statements(
        self,
        text: str,
        concepts: list[dict[str, Any]],
        chunk: dict[str, Any],
        metadata: dict[str, Any],
    ) -> list[dict[str, Any]]:
        if not concepts:
            return []
        sentences = [
            sentence.strip()
            for sentence in re.split(r"(?<=[.!?。！？])\s+", text)
            if sentence.strip()
        ]
        statements = []
        for sentence in sentences:
            sentence_lower = sentence.lower()
            mentioned = [
                concept["canonical_label"]
                for concept in concepts
                if concept["canonical_label"] in sentence_lower
                or concept["label"] in sentence_lower
            ]
            if mentioned:
                statements.append(
                    {
                        "text": sentence,
                        "concepts": sorted(set(mentioned)),
                        "source_id": metadata.get("source_id"),
                        "chunk_id": chunk.get("chunk_id"),
                    }
                )
        return statements

    def _relation_type(self, text: str) -> str:
        lowered = text.lower()
        for relation_type, markers in RELATION_MARKERS.items():
            if any(marker in lowered for marker in markers):
                return relation_type
        return "MENTIONS"
