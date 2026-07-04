from __future__ import annotations

from fastapi import APIRouter, Query, Request

from dkg_api.app.services.graph_service import GraphService
from dkg_api.app.services.graph_visualization_engine import GraphVisualizationEngine
from dkg_api.app.services.pathfinding_engine import PathfindingEngine

router = APIRouter(tags=["knowledge-map"])


@router.get("/map/{concept_id}")
def knowledge_map(concept_id: str, request: Request) -> dict[str, object]:
    graph = GraphService(request.app.state.neo4j)
    engine = GraphVisualizationEngine()
    return engine.build_map(concept_id, graph.visualization_neighborhood(concept_id))


@router.get("/path")
def path(
    request: Request,
    source_id: str = Query(..., alias="from"),
    target_id: str = Query(..., alias="to"),
) -> dict[str, object]:
    graph = GraphService(request.app.state.neo4j)
    engine = PathfindingEngine()
    return {
        "from": source_id,
        "to": target_id,
        "path": engine.build_path(graph.path_between(source_id, target_id)),
    }


@router.get("/overlay/{concept_id}")
def overlay(concept_id: str, request: Request) -> dict[str, object]:
    graph = GraphService(request.app.state.neo4j)
    engine = GraphVisualizationEngine()
    return engine.build_overlay(
        concept_id, graph.visualization_neighborhood(concept_id)
    )


@router.get("/clusters/{concept_id}")
def clusters(concept_id: str, request: Request) -> dict[str, object]:
    graph = GraphService(request.app.state.neo4j)
    engine = GraphVisualizationEngine()
    return engine.build_clusters(
        concept_id, graph.visualization_neighborhood(concept_id)
    )
