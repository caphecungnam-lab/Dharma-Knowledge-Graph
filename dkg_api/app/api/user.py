from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query, Request
from pydantic import BaseModel, Field

from dkg_api.app.services.adaptive_explainer import AdaptiveExplainer
from dkg_api.app.services.dharma_path_engine import DharmaPathEngine
from dkg_api.app.services.epistemic_truth_system import EpistemicTruthSystem
from dkg_api.app.services.graph_service import GraphService
from dkg_api.app.services.learning_state_tracker import LearningStateTracker
from dkg_api.app.services.progression_mapper import ProgressionMapper
from dkg_api.app.services.user_epistemic_model import UserEpistemicModel

router = APIRouter(tags=["learning-intelligence"])
state_tracker = LearningStateTracker()


class LearningStateUpdate(BaseModel):
    user_id: str = Field(..., min_length=1)
    seen_nodes: list[str] = Field(default_factory=list)
    mastered_nodes: list[str] = Field(default_factory=list)
    confused_nodes: list[str] = Field(default_factory=list)


@router.get("/user/profile/{user_id}")
def profile(user_id: str) -> dict[str, Any]:
    return UserEpistemicModel().profile_user(user_id)


@router.post("/user/update-state")
def update_state(payload: LearningStateUpdate) -> dict[str, Any]:
    return state_tracker.update_state(
        payload.user_id,
        seen_nodes=payload.seen_nodes,
        mastered_nodes=payload.mastered_nodes,
        confused_nodes=payload.confused_nodes,
    )


@router.get("/path/generate")
def generate_path(user_id: str = Query(..., min_length=1)) -> dict[str, Any]:
    profile_data = UserEpistemicModel().profile_user(user_id)
    learning_state = state_tracker.state_for(user_id)
    return DharmaPathEngine().generate_path(profile_data, learning_state)


@router.get("/explain/{concept}")
def explain(concept: str, request: Request, user_id: str = Query(...)) -> dict[str, Any]:
    profile_data = UserEpistemicModel().profile_user(user_id)
    context = _validated_context(concept, request)
    return AdaptiveExplainer().explain(concept, profile_data, context)


@router.get("/progress/{user_id}")
def progress(user_id: str) -> dict[str, Any]:
    profile_data = UserEpistemicModel().profile_user(user_id)
    learning_state = state_tracker.state_for(user_id)
    return ProgressionMapper().map_progress(profile_data, learning_state)


def _validated_context(concept: str, request: Request) -> list[dict[str, Any]]:
    graph = GraphService(request.app.state.neo4j)
    try:
        graph_data = graph.visualization_neighborhood(concept)
    except Exception:
        return []

    graph_vector_context = []
    for node in graph_data.get("nodes", []):
        graph_vector_context.append(
            {
                "match": {
                    "node_id": node.get("id"),
                    "label": node.get("label"),
                    "definition": node.get("definition"),
                    "tradition": node.get("tradition"),
                    "score": node.get("confidence", 0.5),
                    "source_id": node.get("source_id"),
                    "source_type": node.get("source_type"),
                },
                "related": _related_for_node(node.get("id"), graph_data),
            }
        )

    truth_system = EpistemicTruthSystem()
    return truth_system.filter_ai_usable(truth_system.evaluate(graph_vector_context))


def _related_for_node(
    node_id: str | None,
    graph_data: dict[str, Any],
) -> list[dict[str, Any]]:
    if not node_id:
        return []
    related_ids = set()
    for edge in graph_data.get("edges", []):
        if edge.get("from") == node_id:
            related_ids.add(edge.get("to"))
        if edge.get("to") == node_id:
            related_ids.add(edge.get("from"))

    nodes = []
    for node in graph_data.get("nodes", []):
        if node.get("id") in related_ids:
            nodes.append(node)
    return nodes
