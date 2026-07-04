from __future__ import annotations

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

from dkg_api.app.services.graph_service import GraphService
from dkg_api.app.services.vector_service import VectorService

router = APIRouter(prefix="/ai", tags=["ai"])


class AskIn(BaseModel):
    query: str = Field(..., min_length=1)


@router.post("/ask")
def ask(payload: AskIn, request: Request) -> dict[str, object]:
    graph = GraphService(request.app.state.neo4j)
    vector = VectorService(request.app.state.qdrant)

    matches = vector.search(payload.query)
    merged_results = []
    for match in matches:
        node_id = str(match.get("node_id", ""))
        related = graph.related_concepts(node_id) if node_id else []
        merged_results.append(
            {
                "match": match,
                "related": related,
            }
        )

    return {
        "query": payload.query,
        "results": merged_results,
    }
