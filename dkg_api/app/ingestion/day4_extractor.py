from __future__ import annotations

import re
from typing import Any


EXPLICIT_CONCEPT_PATTERNS = {
    "impermanence": ["impermanence", "anicca", "vô thường"],
    "suffering": ["suffering", "dukkha", "khổ"],
    "non-self": ["non-self", "anatta", "vô ngã"],
    "karma": ["karma", "kamma", "nghiệp"],
    "rebirth": ["rebirth", "tái sinh"],
    "nirvana": ["nirvana", "nibbana", "niết bàn"],
    "emptiness": ["emptiness", "sunyata", "śūnyatā", "tánh không"],
    "death": ["death", "dying", "cái chết", "chết"],
    "bardo": ["bardo"],
    "kinh_sau_sau": ["kinh 66", "kinh sáu sáu", "kinh sáu sáu"],
    "six_sense_bases": ["sáu căn", "lục căn"],
    "six_sense_objects": ["sáu trần", "lục trần"],
    "six_consciousnesses": ["sáu thức", "lục thức"],
}

EXPLICIT_RELATION_MARKERS = {
    "RELATED_TO": ["related to", "connected to", "liên hệ"],
    "CONTRASTS_WITH": ["contrasts with", "differs from", "khác với"],
    "PREREQUISITE_FOR": ["prerequisite for", "điều kiện cho"],
}


class Day4Extractor:
    """
    Strict real-corpus extractor.

    It only emits candidates when a known concept string appears verbatim in the
    source text. Relations are emitted only when a relation marker is explicit in
    the same sentence. Co-occurrence alone is not treated as a doctrine claim.
    """

    def extract(
        self,
        chunk: dict[str, Any],
        source_metadata: dict[str, Any] | None = None,
    ) -> dict[str, list[dict[str, Any]]]:
        metadata = source_metadata or {}
        text = str(chunk.get("text") or "")
        sentences = self._sentences(text)
        concepts = self._concepts(sentences, chunk, metadata)
        return {
            "concepts": concepts,
            "relations": self._relations(sentences, concepts),
            "statements": self._statements(sentences, concepts, chunk, metadata),
        }

    def _concepts(
        self,
        sentences: list[str],
        chunk: dict[str, Any],
        metadata: dict[str, Any],
    ) -> list[dict[str, Any]]:
        concepts = []
        seen = set()
        for canonical_label, variants in EXPLICIT_CONCEPT_PATTERNS.items():
            for sentence in sentences:
                matched_variant = self._matched_variant(sentence, variants)
                if matched_variant is None:
                    continue
                key = (canonical_label, matched_variant)
                if key in seen:
                    continue
                seen.add(key)
                concepts.append(
                    {
                        "id": f"concept_{canonical_label}",
                        "label": matched_variant,
                        "canonical_label": canonical_label,
                        "definition": sentence,
                        "explicit_text": sentence,
                        "source_id": metadata.get("source_id"),
                        "source_type": metadata.get("source_type", "text"),
                        "tradition": metadata.get("tradition", "unknown"),
                        "chunk_id": chunk.get("chunk_id"),
                        "position": chunk.get("position"),
                        "score": 0.86,
                        "extraction_rule": "explicit_mention_only",
                    }
                )
                break
        return concepts

    def _relations(
        self,
        sentences: list[str],
        concepts: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        relations = []
        for sentence in sentences:
            relation_type = self._relation_type(sentence)
            if relation_type is None:
                continue
            mentioned = [
                concept
                for concept in concepts
                if self._contains(sentence, concept["label"])
                or self._contains(sentence, concept["canonical_label"])
            ]
            for index, source in enumerate(mentioned):
                for target in mentioned[index + 1 :]:
                    relations.append(
                        {
                            "from": source["canonical_label"],
                            "to": target["canonical_label"],
                            "type": relation_type,
                            "evidence_text": sentence,
                        }
                    )
        return relations

    def _statements(
        self,
        sentences: list[str],
        concepts: list[dict[str, Any]],
        chunk: dict[str, Any],
        metadata: dict[str, Any],
    ) -> list[dict[str, Any]]:
        statements = []
        for sentence in sentences:
            mentioned = [
                concept["canonical_label"]
                for concept in concepts
                if self._contains(sentence, concept["label"])
                or self._contains(sentence, concept["canonical_label"])
            ]
            if mentioned:
                statements.append(
                    {
                        "text": sentence,
                        "concepts": sorted(set(mentioned)),
                        "source_id": metadata.get("source_id"),
                        "chunk_id": chunk.get("chunk_id"),
                        "explicit": True,
                    }
                )
        return statements

    def _matched_variant(self, sentence: str, variants: list[str]) -> str | None:
        for variant in variants:
            if self._contains(sentence, variant):
                return variant
        return None

    def _contains(self, text: str, term: str) -> bool:
        if not term:
            return False
        return term.lower() in text.lower()

    def _relation_type(self, sentence: str) -> str | None:
        lowered = sentence.lower()
        for relation_type, markers in EXPLICIT_RELATION_MARKERS.items():
            if any(marker in lowered for marker in markers):
                return relation_type
        return None

    def _sentences(self, text: str) -> list[str]:
        sentences = [
            sentence.strip()
            for sentence in re.split(r"(?<=[.!?。！？])\s+", text)
            if sentence.strip()
        ]
        return sentences or ([text.strip()] if text.strip() else [])
