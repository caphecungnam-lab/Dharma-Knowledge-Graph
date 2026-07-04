from __future__ import annotations

import os
from typing import Any

from qdrant_client import QdrantClient as QdrantSDKClient
from qdrant_client.http import models

COLLECTION_NAME = "dkg_embeddings"
VECTOR_SIZE = 128


class QdrantClient:
    def __init__(self) -> None:
        host = os.getenv("QDRANT_HOST", "localhost")
        port = int(os.getenv("QDRANT_PORT", "6333"))
        self.client = QdrantSDKClient(host=host, port=port)

    def health(self) -> dict[str, object]:
        try:
            self.client.get_collections()
            return {"ok": True}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def ensure_collection(self) -> None:
        try:
            self.client.get_collection(COLLECTION_NAME)
            return
        except Exception:
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(
                    size=VECTOR_SIZE,
                    distance=models.Distance.COSINE,
                ),
            )

    def upsert_point(
        self,
        point_id: str,
        vector: list[float],
        payload: dict[str, Any],
    ) -> None:
        self.ensure_collection()
        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                models.PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload,
                )
            ],
        )

    def search(self, vector: list[float], limit: int = 5) -> list[Any]:
        self.ensure_collection()
        return self.client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=limit,
            with_payload=True,
        )
