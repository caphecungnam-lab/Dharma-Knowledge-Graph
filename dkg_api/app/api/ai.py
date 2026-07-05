from __future__ import annotations

from time import perf_counter

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field, field_validator

from dkg_api.app.cache.query_cache import query_cache
from dkg_api.app.observability.logger import get_logger
from dkg_api.app.observability.metrics import metrics
from dkg_api.app.security.input_sanitizer import sanitize_text
from dkg_api.app.services.graph_service import GraphService
from dkg_api.app.services.orchestrator import AIOrchestrator
from dkg_api.app.services.vector_service import VectorService

router = APIRouter(prefix="/ai", tags=["ai"])
logger = get_logger(__name__)


class AskIn(BaseModel):
    query: str = Field(..., min_length=1)

    @field_validator("query")
    @classmethod
    def sanitize_query(cls, value: str) -> str:
        return sanitize_text(value, max_length=500)


@router.post("/ask")
def ask(payload: AskIn, request: Request) -> dict[str, object]:
    started_at = perf_counter()

    def finalize(response: dict[str, object]) -> dict[str, object]:
        metrics.record_latency((perf_counter() - started_at) * 1000)
        return response

    cached = query_cache.get(payload.query)
    if cached is not None:
        cached["cache"] = {"hit": True}
        return finalize(cached)

    graph = GraphService(request.app.state.neo4j)
    vector = VectorService(request.app.state.qdrant)
    orchestrator = AIOrchestrator(graph=graph, vector=vector)
    answer = orchestrator.answer(payload.query)
    if answer.get("status") in {"rejected", "critical_safety_failure"}:
        logger.info("query stopped by safety orchestrator: %s", answer)
        return finalize(answer)

    answer["cache"] = {"hit": False}
    query_cache.set(
        payload.query,
        answer,
        ttl_seconds=query_cache.ttl_for_context(
            answer.get("sanitized_context") or []
        ),
    )
    return finalize(answer)
