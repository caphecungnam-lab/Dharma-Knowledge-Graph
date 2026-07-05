from __future__ import annotations

import json
from statistics import mean

from day1_common import SAMPLE_QUERIES, elapsed_ms, neo4j_search, now_ms, post_json, qdrant_search, truth_filter_count


def collect() -> dict[str, object]:
    rows = []
    for query in SAMPLE_QUERIES * 2:
        started_total = now_ms()

        started_api = now_ms()
        _, api_error = post_json("/ai/ask", {"query": query})
        api_ms = elapsed_ms(started_api)

        started_retrieval = now_ms()
        qdrant_results, qdrant_error = qdrant_search(query)
        neo4j_nodes, neo4j_error = neo4j_search(query)
        retrieval_ms = elapsed_ms(started_retrieval)

        started_truth = now_ms()
        _, after_truth, truth_error = truth_filter_count(qdrant_results + neo4j_nodes)
        truth_ms = elapsed_ms(started_truth)

        total_ms = elapsed_ms(started_total)
        ai_ms = max(api_ms - retrieval_ms - truth_ms, 0.0)
        rows.append(
            {
                "query": query,
                "api_response_ms": api_ms,
                "retrieval_ms": retrieval_ms,
                "truth_engine_ms": truth_ms,
                "ai_ms": round(ai_ms, 3),
                "total_pipeline_ms": total_ms,
                "after_truth_filter": after_truth,
                "errors": [error for error in (api_error, qdrant_error, neo4j_error, truth_error) if error],
            }
        )

    total_values = [row["total_pipeline_ms"] for row in rows]
    stage_averages = {
        "retrieval": mean(row["retrieval_ms"] for row in rows),
        "truth_engine": mean(row["truth_engine_ms"] for row in rows),
        "ai": mean(row["ai_ms"] for row in rows),
    }
    bottleneck_stage = max(stage_averages, key=stage_averages.get)
    if stage_averages[bottleneck_stage] <= 0:
        bottleneck_stage = "other"
    return {
        "avg_latency_ms": round(mean(total_values), 3),
        "max_latency_ms": round(max(total_values), 3),
        "min_latency_ms": round(min(total_values), 3),
        "bottleneck_stage": bottleneck_stage,
        "stage_averages_ms": {key: round(value, 3) for key, value in stage_averages.items()},
        "samples": rows,
    }


def main() -> int:
    payload = collect()
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
