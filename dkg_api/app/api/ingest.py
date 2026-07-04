from __future__ import annotations

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

from dkg_api.app.services.graph_service import GraphService
from dkg_api.app.services.vector_service import VectorService

router = APIRouter(prefix="/ingest", tags=["ingest"])


class ConceptIn(BaseModel):
    id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    definition: str = Field(..., min_length=1)
    tradition: str = Field(..., min_length=1)


@router.post("/concept")
def ingest_concept(payload: ConceptIn, request: Request) -> dict[str, object]:
    concept = payload.model_dump()
    graph = GraphService(request.app.state.neo4j)
    vector = VectorService(request.app.state.qdrant)

    graph.upsert_concept(concept)
    vector.upsert_concept(concept)

    return {
        "status": "ok",
        "concept": concept,
    }
