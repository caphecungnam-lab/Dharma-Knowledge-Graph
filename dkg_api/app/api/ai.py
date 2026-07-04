from __future__ import annotations

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

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
    truth_system = EpistemicTruthSystem()
    reasoner = AIReasoner()

    matches = vector.search(payload.query)
    graph_vector_context = []
    for match in matches:
        node_id = str(match.get("node_id", ""))
        related = graph.related_concepts(node_id) if node_id else []
        graph_vector_context.append(
            {
                "match": match,
                "related": related,
            }
        )

    evaluations = truth_system.evaluate(graph_vector_context)
    validated_context = truth_system.filter_ai_usable(evaluations)
    return reasoner.generate(payload.query, validated_context)
