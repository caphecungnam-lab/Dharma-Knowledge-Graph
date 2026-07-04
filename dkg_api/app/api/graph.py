from __future__ import annotations

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

from dkg_api.app.services.graph_service import GraphService

router = APIRouter(prefix="/graph", tags=["graph"])


class ExpandIn(BaseModel):
    node_id: str = Field(..., min_length=1)


@router.post("/expand")
def expand(payload: ExpandIn, request: Request) -> dict[str, object]:
    graph = GraphService(request.app.state.neo4j)
    return graph.expand_node(payload.node_id)


@router.post("/contradictions")
def contradictions(request: Request) -> dict[str, object]:
    graph = GraphService(request.app.state.neo4j)
    return {
        "contradictions": graph.contradictions(),
    }


@router.get("/evolution")
def evolution(request: Request) -> dict[str, object]:
    graph = GraphService(request.app.state.neo4j)
    return graph.evolution()
