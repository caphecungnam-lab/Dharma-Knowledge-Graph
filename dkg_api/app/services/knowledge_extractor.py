from __future__ import annotations

import re
from typing import Any

from dkg_api.app.services.tradition_mapper import TraditionMapper

CONCEPT_KEYWORDS = {
    "impermanence": ["impermanence", "anicca", "vô thường"],
    "suffering": ["suffering", "dukkha", "khổ"],
    "death": ["death", "dying", "bardo", "chết"],
    "nirvana": ["nirvana", "nibbana", "niết bàn"],
    "bardo": ["bardo"],
    "emptiness": ["emptiness", "sunyata", "śūnyatā", "tánh không"],
}

PRACTICE_KEYWORDS = {
    "meditation": ["meditation", "samadhi", "thiền"],
    "chanting": ["chanting", "recitation", "tụng"],
    "visualization": ["visualization", "quán tưởng"],
    "ethics": ["ethics", "sila", "precepts", "giới"],
}


class KnowledgeExtractor:
    def __init__(self) -> None:
        self.tradition_mapper = TraditionMapper()

    def split_into_chunks(
        self, raw_text: str, max_words: int = 90
    ) -> list[dict[str, str]]:
        sentences = [
            sentence.strip()
            for sentence in re.split(r"(?<=[.!?。！？])\s+", raw_text)
            if sentence.strip()
        ]
        chunks: list[dict[str, str]] = []
        current: list[str] = []

        for sentence in sentences or [raw_text.strip()]:
            if len(" ".join(current + [sentence]).split()) > max_words and current:
                chunks.append(
                    {
                        "id": f"chunk_{len(chunks) + 1:04d}",
                        "text": " ".join(current),
                    }
                )
                current = []
            if sentence:
                current.append(sentence)

        if current:
            chunks.append(
                {
                    "id": f"chunk_{len(chunks) + 1:04d}",
                    "text": " ".join(current),
                }
            )

        return chunks

    def extract_candidates(
        self,
        chunks: list[dict[str, str]],
        source_metadata: dict[str, Any],
    ) -> dict[str, list[dict[str, Any]]]:
        candidates = []
        relations = []
        for chunk in chunks:
            chunk_candidates = self._extract_chunk_candidates(chunk, source_metadata)
            candidates.extend(chunk_candidates)
            relations.extend(self._relations_for_chunk(chunk_candidates, chunk["text"]))

        return {
            "nodes": self._dedupe_nodes(candidates),
            "relations": relations,
        }

    def detect_concepts(
        self,
        chunks: list[dict[str, str]],
        source_metadata: dict[str, Any],
    ) -> list[dict[str, Any]]:
        extracted = self.extract_candidates(chunks, source_metadata)
        return [node for node in extracted["nodes"] if node["node_type"] == "Concept"]

    def detect_practices(
        self,
        chunks: list[dict[str, str]],
        source_metadata: dict[str, Any],
    ) -> list[dict[str, Any]]:
        extracted = self.extract_candidates(chunks, source_metadata)
        return [node for node in extracted["nodes"] if node["node_type"] == "Practice"]

    def _extract_chunk_candidates(
        self,
        chunk: dict[str, str],
        source_metadata: dict[str, Any],
    ) -> list[dict[str, Any]]:
        text = chunk["text"]
        lowered = text.lower()
        candidates = []
        source_id = str(source_metadata.get("source_id") or "source_text")
        source_type = str(source_metadata.get("source_type") or "text")
        tradition = self.tradition_mapper.map_tradition(text, source_metadata)

        for label, keywords in CONCEPT_KEYWORDS.items():
            if any(keyword in lowered for keyword in keywords):
                candidates.append(
                    self._candidate(
                        node_type="Concept",
                        label=label,
                        text=text,
                        tradition=tradition,
                        source_id=source_id,
                        source_type=source_type,
                        chunk_id=chunk["id"],
                    )
                )

        for label, keywords in PRACTICE_KEYWORDS.items():
            if any(keyword in lowered for keyword in keywords):
                candidates.append(
                    self._candidate(
                        node_type="Practice",
                        label=label,
                        text=text,
                        tradition=tradition,
                        source_id=source_id,
                        source_type=source_type,
                        chunk_id=chunk["id"],
                    )
                )

        return candidates

    def _candidate(
        self,
        node_type: str,
        label: str,
        text: str,
        tradition: str,
        source_id: str,
        source_type: str,
        chunk_id: str,
    ) -> dict[str, Any]:
        node_id = f"{node_type.lower()}_{label.replace(' ', '_')}"
        return {
            "node_id": node_id,
            "node_type": node_type,
            "label": label,
            "definition": text,
            "tradition": tradition,
            "source_id": source_id,
            "source_type": source_type,
            "chunk_id": chunk_id,
            "text": text,
            "score": 0.85,
        }

    def _relations_for_chunk(
        self,
        candidates: list[dict[str, Any]],
        chunk_text: str,
    ) -> list[dict[str, str]]:
        relations = []
        lowered = chunk_text.lower()
        relation_type = "RELATED_TO"
        if "prerequisite" in lowered or "requires" in lowered:
            relation_type = "PREREQUISITE_FOR"
        if "interpreted as" in lowered:
            relation_type = "INTERPRETED_AS"

        for index, source in enumerate(candidates):
            for target in candidates[index + 1 :]:
                relations.append(
                    {
                        "source": source["node_id"],
                        "target": target["node_id"],
                        "type": relation_type,
                    }
                )
        return relations

    def _dedupe_nodes(self, nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
        by_id: dict[str, dict[str, Any]] = {}
        for node in nodes:
            by_id.setdefault(node["node_id"], node)
        return list(by_id.values())
