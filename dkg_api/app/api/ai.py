from __future__ import annotations

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

from dkg_api.app.safety.context_sanitizer import ContextSanitizer
from dkg_api.app.safety.epistemic_gateway import EpistemicGateway
from dkg_api.app.safety.output_validator import OutputValidator
from dkg_api.app.safety.retrieval_control_layer import RetrievalControlLayer
from dkg_api.app.safety.safety_policy import INSUFFICIENT_EPISTEMIC_DATA
from dkg_api.app.services.ai_reasoner import AIReasoner
from dkg_api.app.services.epistemic_truth_system import EpistemicTruthSystem
from dkg_api.app.services.graph_service import GraphService
from dkg_api.app.services.vector_service import VectorService

router = APIRouter(prefix="/ai", tags=["ai"])


class AskIn(BaseModel):
    query: str = Field(..., min_length=1)


@router.post("/ask")
def ask(payload: AskIn, request: Request) -> dict[str, object]:
    graph = GraphService(request.app.state.neo4j)
    vector = VectorService(request.app.state.qdrant)
    gateway = EpistemicGateway()
    retrieval = RetrievalControlLayer()
    truth_system = EpistemicTruthSystem()
    sanitizer = ContextSanitizer()
    reasoner = AIReasoner()
    validator = OutputValidator()

    query_classification = gateway.classify_query(payload.query)
    if query_classification["mode"] == "reject":
        return {
            "answer": INSUFFICIENT_EPISTEMIC_DATA,
            "confidence": 0.0,
            "safety": {
                "gateway": query_classification,
                "stopped_at": "epistemic_gateway",
            },
        }

    graph_vector_context = retrieval.fetch(payload.query, vector, graph)
    evaluations = truth_system.evaluate(graph_vector_context)
    validated_context = sanitizer.sanitize(
        truth_system.filter_ai_usable(evaluations),
        allowed_layers=query_classification["allowed_layers"],
    )
    if not validated_context:
        return {
            "answer": INSUFFICIENT_EPISTEMIC_DATA,
            "confidence": 0.0,
            "safety": {
                "gateway": query_classification,
                "stopped_at": "context_sanitizer",
            },
        }

    answer = reasoner.generate(payload.query, validated_context)
    validation = validator.validate(answer, validated_context)
    if validation["status"] != "APPROVED":
        return {
            "answer": INSUFFICIENT_EPISTEMIC_DATA,
            "confidence": 0.0,
            "safety": {
                "gateway": query_classification,
                "output_validation": validation,
                "stopped_at": "output_validator",
            },
        }

    answer["safety"] = {
        "gateway": query_classification,
        "output_validation": validation,
    }
    return answer
