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
            "source_id": concept.get("source_id"),
            "source_url": concept.get("source_url"),
            "source_type": concept.get("source_type"),
            "citation_id": concept.get("citation_id"),
        }
        self.client.upsert_point(
            point_id=self.point_id_for_node(concept["id"]),
            vector=embed_text(text),
            payload=payload,
        )

    def upsert_concepts(self, concepts: list[dict[str, str]]) -> None:
        points = []
        for concept in concepts:
            payload = {
                "node_id": concept["id"],
                "text": concept["definition"],
                "tradition": concept["tradition"],
                "source_id": concept.get("source_id"),
                "source_url": concept.get("source_url"),
                "source_type": concept.get("source_type"),
                "citation_id": concept.get("citation_id"),
            }
            points.append(
                {
                    "point_id": self.point_id_for_node(concept["id"]),
                    "vector": embed_text(concept["definition"]),
                    "payload": payload,
                }
            )
        self.client.upsert_points(points)

    def search(self, query: str, limit: int | None = None) -> list[dict[str, Any]]:
        top_k = limit if limit is not None else self._adaptive_top_k(query)
        results = self.client.search(embed_text(query), limit=top_k)
        matches: list[dict[str, Any]] = []
        for result in results:
            payload = result.payload or {}
            matches.append(
                {
                    "score": result.score,
                    "node_id": payload.get("node_id"),
                    "text": payload.get("text"),
                    "tradition": payload.get("tradition"),
                    "source_id": payload.get("source_id"),
                    "source_url": payload.get("source_url"),
                    "source_type": payload.get("source_type"),
                    "citation_id": payload.get("citation_id"),
                }
            )
        return matches

    def _adaptive_top_k(self, query: str) -> int:
        token_count = len(query.split())
        if token_count <= 5:
            return 5
        return 15
