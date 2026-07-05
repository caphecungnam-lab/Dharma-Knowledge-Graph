from __future__ import annotations

import json

from day1_common import SAMPLE_QUERIES, neo4j_search, qdrant_search, truth_filter_count


def collect() -> dict[str, object]:
    rows = []
    for query in SAMPLE_QUERIES:
        qdrant_results, qdrant_error = qdrant_search(query)
        neo4j_nodes, neo4j_error = neo4j_search(query)
        evaluated_count, after_truth, truth_error = truth_filter_count(qdrant_results + neo4j_nodes)
        rejection_rate = (
            (evaluated_count - after_truth) / evaluated_count
            if evaluated_count
            else 0.0
        )
        rows.append(
            {
                "query": query,
                "neo4j_nodes": len(neo4j_nodes),
                "qdrant_results": len(qdrant_results),
                "after_truth_filter": after_truth,
                "rejection_rate": round(rejection_rate, 3),
                "errors": [error for error in (qdrant_error, neo4j_error, truth_error) if error],
            }
        )
    return {
        "queries": rows,
        "avg_rejection_rate": round(
            sum(row["rejection_rate"] for row in rows) / len(rows),
            3,
        ),
    }


def main() -> int:
    payload = collect()
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
