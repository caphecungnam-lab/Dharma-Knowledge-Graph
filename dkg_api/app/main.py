from __future__ import annotations

from fastapi import FastAPI

from dkg_api.app.api.ai import router as ai_router
from dkg_api.app.api.graph import router as graph_router
from dkg_api.app.api.ingest import router as ingest_router
from dkg_api.app.api.map import router as map_router
from dkg_api.app.api.user import router as user_router
from dkg_api.app.db.neo4j_client import Neo4jClient
from dkg_api.app.db.qdrant_client import QdrantClient

app = FastAPI(title="Dharma Knowledge Graph API", version="0.1.0")

app.include_router(ai_router)
app.include_router(graph_router)
app.include_router(ingest_router)
app.include_router(map_router)
app.include_router(user_router)


@app.on_event("startup")
def startup() -> None:
    qdrant = QdrantClient()
    try:
        qdrant.ensure_collection()
    except Exception:
        pass
    app.state.neo4j = Neo4jClient()
    app.state.qdrant = qdrant


@app.on_event("shutdown")
def shutdown() -> None:
    neo4j = getattr(app.state, "neo4j", None)
    if neo4j is not None:
        neo4j.close()


@app.get("/health")
def health() -> dict[str, object]:
    neo4j = getattr(app.state, "neo4j", None) or Neo4jClient()
    qdrant = getattr(app.state, "qdrant", None) or QdrantClient()
    neo4j_status = neo4j.health()
    qdrant_status = qdrant.health()
    return {
        "status": "ok" if neo4j_status["ok"] and qdrant_status["ok"] else "degraded",
        "neo4j": neo4j_status,
        "qdrant": qdrant_status,
    }
