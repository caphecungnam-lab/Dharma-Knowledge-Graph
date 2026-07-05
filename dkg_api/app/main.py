from __future__ import annotations

from fastapi import FastAPI
from starlette.responses import PlainTextResponse

from dkg_api.app.api.ai import router as ai_router
from dkg_api.app.api.graph import router as graph_router
from dkg_api.app.api.ingest import router as ingest_router
from dkg_api.app.api.map import router as map_router
from dkg_api.app.api.user import router as user_router
from dkg_api.app.db.neo4j_client import Neo4jClient
from dkg_api.app.db.qdrant_client import QdrantClient
from dkg_api.app.db.redis_client import RedisClient
from dkg_api.app.cache.embedding_cache import embedding_cache
from dkg_api.app.cache.graph_cache import graph_cache
from dkg_api.app.cache.query_cache import query_cache
from dkg_api.app.observability.metrics import metrics
from dkg_api.app.safety.injection_guard import InjectionGuardMiddleware
from dkg_api.app.security.middleware import ApiKeyAndRateLimitMiddleware
from dkg_api.app.services.epistemic_truth_system import EpistemicTruthSystem

app = FastAPI(title="Dharma Knowledge Graph API", version="0.1.0")
app.add_middleware(InjectionGuardMiddleware)
app.add_middleware(ApiKeyAndRateLimitMiddleware)

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
    neo4j = Neo4jClient()
    try:
        neo4j.ensure_indexes()
    except Exception:
        pass
    app.state.neo4j = neo4j
    app.state.qdrant = qdrant
    app.state.redis = RedisClient()


@app.on_event("shutdown")
def shutdown() -> None:
    neo4j = getattr(app.state, "neo4j", None)
    if neo4j is not None:
        neo4j.close()


@app.get("/health")
def health() -> dict[str, object]:
    neo4j = getattr(app.state, "neo4j", None) or Neo4jClient()
    qdrant = getattr(app.state, "qdrant", None) or QdrantClient()
    redis = getattr(app.state, "redis", None) or RedisClient()
    neo4j_status = neo4j.health()
    qdrant_status = qdrant.health()
    redis_status = redis.health()
    truth_status = truth_engine_health()
    cache_status = "ok" if query_cache.stats()["max_size"] > 0 else "fail"
    all_ok = all(
        [
            neo4j_status["ok"],
            qdrant_status["ok"],
            redis_status["ok"],
            truth_status == "ok",
            cache_status == "ok",
        ]
    )
    return {
        "api": "ok",
        "status": "ok" if all_ok else "fail",
        "neo4j": neo4j_status,
        "qdrant": qdrant_status,
        "redis": redis_status,
        "truth_engine": truth_status,
        "cache_status": cache_status,
        "cache": {
            "query": query_cache.stats(),
            "graph": graph_cache.stats(),
            "embedding": embedding_cache.stats(),
        },
        "runtime": metrics.health_metrics(),
    }


@app.get("/metrics")
def system_metrics() -> dict[str, object]:
    runtime = metrics.health_metrics()
    cache = query_cache.stats()
    detailed = metrics.metrics()
    return {
        "avg_latency_ms": runtime["latency_avg_ms"],
        "truth_rejection_rate": runtime["truth_rejection_rate"],
        "cache_hit_rate": cache["hit_rate"],
        "top_queries": detailed["top_queried_concepts"],
        "epistemic_distribution": detailed["epistemic_distribution"],
        "conflict_frequency": detailed["conflict_frequency"],
        "step_latency_avg_ms": detailed["step_latency_avg_ms"],
    }


@app.get("/metrics/prometheus")
def prometheus_metrics() -> PlainTextResponse:
    return PlainTextResponse(
        metrics.prometheus(cache_hit_rate=query_cache.stats()["hit_rate"]),
        media_type="text/plain; version=0.0.4",
    )


def truth_engine_health() -> str:
    try:
        evaluated = EpistemicTruthSystem().evaluate(
            [
                {
                    "match": {
                        "node_id": "health_truth_engine",
                        "score": 0.9,
                        "text": "Health check context.",
                        "tradition": "theravada",
                        "source_id": "health_check_source",
                        "source_type": "sutta",
                    },
                    "related": [],
                }
            ]
        )
    except Exception:
        return "fail"
    return "ok" if evaluated and evaluated[0].get("ai_usage_allowed") else "fail"
