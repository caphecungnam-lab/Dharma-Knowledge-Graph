from __future__ import annotations

import re


class TextChunker:
    def __init__(self, max_tokens: int = 700) -> None:
        if max_tokens < 50:
            raise ValueError("max_tokens must preserve semantic continuity.")
        self.max_tokens = max_tokens

    def chunk(
        self,
        text: str,
        source_id: str = "source",
    ) -> list[dict[str, object]]:
        sentences = self._sentences(text)
        chunks = []
        current: list[str] = []

        for sentence in sentences:
            candidate = " ".join(current + [sentence])
            if len(candidate.split()) > self.max_tokens and current:
                chunks.append(self._chunk_payload(source_id, chunks, current))
                current = []
            current.append(sentence)

        if current:
            chunks.append(self._chunk_payload(source_id, chunks, current))

        return chunks

    def _sentences(self, text: str) -> list[str]:
        sentences = [
            sentence.strip()
            for sentence in re.split(r"(?<=[.!?。！？])\s+", text)
            if sentence.strip()
        ]
        return sentences or ([text.strip()] if text.strip() else [])

    def _chunk_payload(
        self,
        source_id: str,
        chunks: list[dict[str, object]],
        sentences: list[str],
    ) -> dict[str, object]:
        position = len(chunks)
        return {
            "chunk_id": f"{source_id}_chunk_{position + 1:04d}",
            "text": " ".join(sentences),
            "position": position,
        }
