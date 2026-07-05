from __future__ import annotations

import json
import os
import resource
import statistics
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

API_ASK_URL = "http://localhost:8000/ai/ask"
QUERIES = [
    "karma",
    "death in Buddhism",
    "compare death in Theravada vs Vajrayana",
]


def main() -> int:
    started_at = time.perf_counter()
    latencies = []
    failures = 0
    safety_violations = 0

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [
            executor.submit(send_query, QUERIES[index % len(QUERIES)])
            for index in range(100)
        ]
        for future in as_completed(futures):
            result = future.result()
            latencies.append(result["latency_ms"])
            if result["failed"]:
                failures += 1
            if result["safety_violation"]:
                safety_violations += 1

    payload = {
        "queries": 100,
        "duration_seconds": round(time.perf_counter() - started_at, 3),
        "avg_response_time_ms": round(statistics.mean(latencies), 3),
        "p95_response_time_ms": percentile(latencies, 95),
        "failure_rate": round(failures / 100, 3),
        "safety_violations": safety_violations,
        "memory_mb": memory_mb(),
        "status": "ok" if safety_violations == 0 else "fail",
    }
    print(json.dumps(payload, indent=2))
    return 0 if payload["status"] == "ok" else 1


def send_query(query: str) -> dict[str, object]:
    started_at = time.perf_counter()
    failed = False
    safety_violation = False
    try:
        response = post_json(API_ASK_URL, {"query": query})
        if response.get("status") == "rejected":
            safety_violation = response.get("reason") != "epistemic_safety_violation"
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        failed = True
    return {
        "latency_ms": round((time.perf_counter() - started_at) * 1000, 3),
        "failed": failed,
        "safety_violation": safety_violation,
    }


def post_json(url: str, payload: dict[str, str]) -> dict[str, object]:
    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    api_key = os.getenv("DKG_API_KEY")
    if api_key:
        headers["x-api-key"] = api_key
    request = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def percentile(values: list[float], percentile_value: int) -> float:
    ordered = sorted(values)
    index = int((percentile_value / 100) * (len(ordered) - 1))
    return round(ordered[index], 3)


def memory_mb() -> float:
    return round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, 3)


if __name__ == "__main__":
    raise SystemExit(main())
