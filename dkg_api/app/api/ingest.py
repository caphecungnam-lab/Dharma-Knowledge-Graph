from __future__ import annotations

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field, field_validator

from dkg_api.app.security.input_sanitizer import sanitize_text
from dkg_api.app.services.auto_ingestion_engine import AutoIngestionEngine
from dkg_api.app.services.graph_service import GraphService
from dkg_api.app.services.vector_service import VectorService

router = APIRouter(prefix="/ingest", tags=["ingest"])


class ConceptIn(BaseModel):
    id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    definition: str = Field(..., min_length=1)
    tradition: str = Field(..., min_length=1)
    source_id: str = Field(default="seed_data", min_length=1)
    source_type: str = Field(default="seed_data", min_length=1)

    @field_validator("id", "label", "definition", "tradition", "source_id", "source_type")
    @classmethod
    def sanitize_fields(cls, value: str) -> str:
        return sanitize_text(value)


class TextIn(BaseModel):
    raw_text: str = Field(..., min_length=1)
    source_metadata: dict[str, object] = Field(default_factory=dict)

    @field_validator("raw_text")
    @classmethod
    def sanitize_raw_text(cls, value: str) -> str:
        return sanitize_text(value, max_length=20000)


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


@router.post("/text")
def ingest_text(payload: TextIn, request: Request) -> dict[str, object]:
    graph = GraphService(request.app.state.neo4j)
    engine = AutoIngestionEngine(graph)
    return engine.process_text(payload.raw_text, payload.source_metadata)
