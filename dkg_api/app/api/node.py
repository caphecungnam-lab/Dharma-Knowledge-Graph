from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from dkg_api.app.services.graph_service import GraphService

router = APIRouter(prefix="/node", tags=["node"])


@router.get("/{node_id}")
def node_details(node_id: str, request: Request) -> dict[str, object]:
    graph = GraphService(request.app.state.neo4j)
    details = graph.node_details(node_id)
    if details is None:
        raise HTTPException(status_code=404, detail="node_not_found")
    return details
