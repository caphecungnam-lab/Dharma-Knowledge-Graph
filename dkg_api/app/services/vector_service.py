from __future__ import annotations

import uuid
from typing import Any

from dkg_api.app.db.qdrant_client import QdrantClient
from dkg_api.app.services.embedding_service import embed_text


class VectorService:
    def __init__(self, client: QdrantClient) -> None:
        self.client = client

    def point_id_for_node(self, node_id: str) -> str:
        return str(uuid.uuid5(uuid.NAMESPACE_URL, f"dkg:{node_id}"))

    def upsert_concept(self, concept: dict[str, str]) -> None:
        text = concept["definition"]
        payload = {
            "node_id": concept["id"],
            "text": text,
            "tradition": concept["tradition"],
        }
        self.client.upsert_point(
            point_id=self.point_id_for_node(concept["id"]),
            vector=embed_text(text),
            payload=payload,
        )

    def search(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        results = self.client.search(embed_text(query), limit=limit)
        matches: list[dict[str, Any]] = []
        for result in results:
            payload = result.payload or {}
            matches.append(
                {
                    "score": result.score,
                    "node_id": payload.get("node_id"),
                    "text": payload.get("text"),
                    "tradition": payload.get("tradition"),
                }
            )
        return matches
