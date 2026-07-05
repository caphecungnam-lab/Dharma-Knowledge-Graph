from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

API_URL = os.getenv("DKG_API_URL", "http://localhost:8000")
API_KEY = os.getenv("DKG_API_KEY", "")
SAMPLE_QUERIES = [
    "karma",
    "death in Buddhism",
    "impermanence",
    "nirvana meaning",
    "compare Theravada and Mahayana",
]


def now_ms() -> float:
    return time.perf_counter() * 1000


def elapsed_ms(started_at: float) -> float:
    return round(now_ms() - started_at, 3)


def get_json(path: str, timeout: int = 5) -> tuple[dict[str, Any] | None, str | None]:
    request = urllib.request.Request(
        f"{API_URL}{path}",
        headers=auth_headers(),
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8")), None
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        return None, str(error)


def post_json(
    path: str,
    payload: dict[str, Any],
    timeout: int = 10,
) -> tuple[dict[str, Any] | None, str | None]:
    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json", **auth_headers()}
    request = urllib.request.Request(
        f"{API_URL}{path}",
        data=data,
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8")), None
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        return None, str(error)


def auth_headers() -> dict[str, str]:
    return {"x-api-key": API_KEY} if API_KEY else {}


def status_from_health(payload: dict[str, Any] | None) -> str:
    if not payload:
        return "fail"
    if payload.get("ok") is True or payload.get("status") == "ok":
        return "ok"
    return "fail"


def neo4j_health() -> tuple[str, str | None]:
    try:
        from dkg_api.app.db.neo4j_client import Neo4jClient

        payload = Neo4jClient().health()
        return status_from_health(payload), str(payload.get("error")) if payload.get("error") else None
    except Exception as error:
        return "fail", str(error)


def qdrant_health() -> tuple[str, str | None]:
    try:
        from dkg_api.app.db.qdrant_client import QdrantClient

        payload = QdrantClient().health()
        return status_from_health(payload), str(payload.get("error")) if payload.get("error") else None
    except Exception as error:
        return "fail", str(error)


def redis_health() -> tuple[str, str | None]:
    try:
        from dkg_api.app.db.redis_client import RedisClient

        payload = RedisClient().health()
        return status_from_health(payload), str(payload.get("error")) if payload.get("error") else None
    except Exception as error:
        return "fail", str(error)


def api_health() -> tuple[str, str | None]:
    payload, error = get_json("/health")
    return ("ok", None) if payload and payload.get("api") == "ok" else ("fail", error)


def truth_engine_probe() -> tuple[str, list[dict[str, Any]]]:
    from dkg_api.app.services.epistemic_truth_system import EpistemicTruthSystem

    context = [
        {
            "match": {
                "node_id": "day1_truth_probe",
                "score": 0.91,
                "text": "Impermanence means conditioned things change.",
                "tradition": "theravada",
                "source_id": "day1_probe_source",
                "source_type": "sutta",
            },
            "related": [],
        }
    ]
    evaluated = EpistemicTruthSystem().evaluate(context)
    status = "ok" if evaluated and evaluated[0].get("ai_usage_allowed") else "fail"
    return status, evaluated


def safety_probe() -> dict[str, str]:
    from dkg_api.app.safety.context_sanitizer import ContextSanitizer
    from dkg_api.app.safety.epistemic_gateway import EpistemicGateway
    from dkg_api.app.safety.output_validator import OutputValidator
    from dkg_api.app.services.ai_reasoner import AIReasoner
    from dkg_api.app.services.epistemic_truth_system import EpistemicTruthSystem

    gateway = EpistemicGateway()
    classification = gateway.classify_query("karma")
    gateway_status = "ok" if classification["mode"] != "reject" else "fail"

    unsafe = [
        {
            "match": {
                "node_id": "day1_unsafe_node",
                "score": 0.1,
                "text": "Unsafe untraceable claim.",
                "tradition": "theravada",
            },
            "related": [],
        }
    ]
    evaluated = EpistemicTruthSystem().evaluate(unsafe)
    sanitized = ContextSanitizer().sanitize(
        evaluated,
        allowed_layers=classification["allowed_layers"],
    )
    sanitizer_status = "ok" if sanitized == [] else "fail"
    answer = AIReasoner().generate("karma", sanitized)
    validation = OutputValidator().validate(answer, sanitized)
    validator_status = "ok" if validation["status"] == "REJECTED" else "fail"
    return {
        "safety_gateway": gateway_status,
        "sanitizer": sanitizer_status,
        "validator": validator_status,
    }


def qdrant_search(query: str, limit: int = 10) -> tuple[list[dict[str, Any]], str | None]:
    try:
        from dkg_api.app.db.qdrant_client import QdrantClient
        from dkg_api.app.services.vector_service import VectorService

        results = VectorService(QdrantClient()).search(query, limit=limit)
        return results, None
    except Exception as error:
        return [], str(error)


def neo4j_search(query: str, limit: int = 10) -> tuple[list[dict[str, Any]], str | None]:
    try:
        from dkg_api.app.db.neo4j_client import Neo4jClient
        from dkg_api.app.services.graph_service import GraphService

        results = GraphService(Neo4jClient()).search_concepts(query, limit=limit)
        return results, None
    except Exception as error:
        return [], str(error)


def truth_filter_count(matches: list[dict[str, Any]]) -> tuple[int, int, str | None]:
    try:
        from dkg_api.app.services.epistemic_truth_system import EpistemicTruthSystem

        contexts = [{"match": match, "related": []} for match in matches]
        truth = EpistemicTruthSystem()
        evaluated = truth.evaluate(contexts)
        filtered = truth.filter_ai_usable(evaluated)
        return len(evaluated), len(filtered), None
    except Exception as error:
        return 0, 0, str(error)


def sample_truth_nodes() -> list[dict[str, Any]]:
    return [
        {
            "match": {
                "node_id": "day1_core_fact",
                "score": 0.95,
                "text": "A sutta source describes impermanence.",
                "tradition": "theravada",
                "source_id": "day1_sutta_source",
                "source_type": "sutta",
            },
            "related": [],
        },
        {
            "match": {
                "node_id": "day1_doctrinal",
                "score": 0.82,
                "text": "A commentary explains karma.",
                "tradition": "theravada",
                "source_id": "day1_commentary_source",
                "source_type": "commentary",
            },
            "related": [],
        },
        {
            "match": {
                "node_id": "day1_interpretive",
                "score": 0.76,
                "text": "This interpretation differs across traditions.",
                "tradition": "mahayana",
                "source_id": "day1_interpretive_source",
                "source_type": "commentary",
            },
            "related": [
                {
                    "id": "day1_related_view",
                    "definition": "interpretation differs in commentary",
                    "tradition": "theravada",
                }
            ],
        },
        {
            "match": {
                "node_id": "day1_esoteric",
                "score": 0.74,
                "text": "Bardo appears in a Vajrayana esoteric context.",
                "tradition": "vajrayana",
                "source_id": "day1_tantra_source",
                "source_type": "commentary",
            },
            "related": [],
        },
        {
            "match": {
                "node_id": "day1_unknown",
                "score": 0.9,
                "text": "No source is attached.",
                "tradition": "unknown",
            },
            "related": [],
        },
    ]


def write_report(path: str | Path, payload: dict[str, Any]) -> None:
    report_path = Path(path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def distribution(values: list[str]) -> dict[str, int]:
    return dict(Counter(values))
