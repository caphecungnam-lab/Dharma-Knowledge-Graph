from __future__ import annotations

import json

from day1_common import (
    api_health,
    neo4j_health,
    qdrant_health,
    redis_health,
    safety_probe,
    truth_engine_probe,
)


def collect() -> dict[str, object]:
    api, api_error = api_health()
    neo4j, neo4j_error = neo4j_health()
    qdrant, qdrant_error = qdrant_health()
    redis, redis_error = redis_health()

    try:
        truth_engine, _ = truth_engine_probe()
        truth_error = None
    except Exception as error:
        truth_engine = "fail"
        truth_error = str(error)

    try:
        safety = safety_probe()
    except Exception as error:
        safety = {
            "safety_gateway": "fail",
            "sanitizer": "fail",
            "validator": "fail",
        }
        safety_error = str(error)
    else:
        safety_error = None

    checks = {
        "api": api,
        "neo4j": neo4j,
        "qdrant": qdrant,
        "redis": redis,
        "truth_engine": truth_engine,
        **safety,
    }
    errors = {
        "api": api_error,
        "neo4j": neo4j_error,
        "qdrant": qdrant_error,
        "redis": redis_error,
        "truth_engine": truth_error,
        "safety": safety_error,
    }
    status = "stable" if all(value == "ok" for value in checks.values()) else "unstable"
    return {
        **checks,
        "system_status": status,
        "errors": {key: value for key, value in errors.items() if value},
    }


def main() -> int:
    payload = collect()
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["system_status"] == "stable" else 1


if __name__ == "__main__":
    raise SystemExit(main())
