from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

from dkg_api.app.db.neo4j_client import Neo4jClient
from dkg_api.app.db.qdrant_client import QdrantClient
from dkg_api.app.db.redis_client import RedisClient
from dkg_api.app.safety.context_sanitizer import ContextSanitizer
from dkg_api.app.safety.epistemic_gateway import EpistemicGateway
from dkg_api.app.safety.output_validator import OutputValidator
from dkg_api.app.services.ai_reasoner import AIReasoner
from dkg_api.app.services.epistemic_truth_system import EpistemicTruthSystem

API_HEALTH_URL = "http://localhost:8000/health"


def main() -> int:
    result = {
        "neo4j": status_from_health(Neo4jClient().health()),
        "qdrant": status_from_health(QdrantClient().health()),
        "redis": status_from_health(RedisClient().health()),
        "api": api_status(API_HEALTH_URL),
        "truth_engine": truth_engine_status(),
        "safety_layer": safety_layer_status(),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if all(value == "ok" for value in result.values()) else 1


def status_from_health(payload: dict[str, object]) -> str:
    return "ok" if payload.get("ok") is True else "fail"


def api_status(url: str) -> str:
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return "ok" if response.status == 200 else "fail"
    except (urllib.error.URLError, TimeoutError):
        return "fail"


def truth_engine_status() -> str:
    context = [
        {
            "match": {
                "node_id": "concept_dukkha",
                "score": 0.95,
                "text": "Dukkha means unsatisfactoriness.",
                "tradition": "theravada",
                "source_id": "source_sutta_001",
                "source_type": "sutta",
            },
            "related": [],
        }
    ]
    try:
        evaluated = EpistemicTruthSystem().evaluate(context)
    except Exception:
        return "fail"
    return "ok" if evaluated and evaluated[0].get("ai_usage_allowed") else "fail"


def safety_layer_status() -> str:
    gateway = EpistemicGateway().classify_query("What is dukkha?")
    evaluated = EpistemicTruthSystem().evaluate(
        [
            {
                "match": {
                    "node_id": "fake_node",
                    "score": 0.1,
                    "text": "Unsafe untraceable claim.",
                    "tradition": "theravada",
                },
                "related": [],
            }
        ]
    )
    sanitized = ContextSanitizer().sanitize(
        evaluated,
        allowed_layers=gateway["allowed_layers"],
    )
    answer = AIReasoner().generate("What is dukkha?", sanitized)
    validation = OutputValidator().validate(answer, sanitized)
    if sanitized:
        return "fail"
    return "ok" if validation["status"] == "REJECTED" else "fail"


if __name__ == "__main__":
    raise SystemExit(main())
