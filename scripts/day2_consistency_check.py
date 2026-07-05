from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def collect() -> dict[str, object]:
    graph_node_ids, graph_stats, graph_error = graph_snapshot()
    embedding_node_ids, embedding_error = embedding_snapshot()
    embedding_mismatch = len(graph_node_ids.symmetric_difference(embedding_node_ids))
    invalid_nodes = graph_stats.get("invalid_nodes", 0)
    orphan_nodes = graph_stats.get("orphan_nodes", 0)
    risk_level = risk_for(orphan_nodes, embedding_mismatch, invalid_nodes, graph_error, embedding_error)
    return {
        "orphan_nodes": orphan_nodes,
        "embedding_mismatch": embedding_mismatch,
        "invalid_nodes": invalid_nodes,
        "risk_level": risk_level,
        "details": {
            "graph_nodes": len(graph_node_ids),
            "embedding_nodes": len(embedding_node_ids),
            "graph_error": graph_error,
            "embedding_error": embedding_error,
        },
    }


def graph_snapshot() -> tuple[set[str], dict[str, int], str | None]:
    try:
        from dkg_api.app.db.neo4j_client import Neo4jClient

        client = Neo4jClient()
        rows = client.execute_read(
            """
            MATCH (n)
            WHERE n:Concept OR n:Practice
            RETURN n.id AS id,
                   CASE WHEN (n)--() THEN false ELSE true END AS orphan,
                   CASE WHEN n.epistemic_type IS NULL
                          OR NOT n.epistemic_type IN ["core_fact", "doctrinal", "interpretive", "esoteric", "unknown", "doctrinal_view", "interpretive_view", "esoteric_view"]
                          OR (n.source_id IS NULL AND n.last_source_id IS NULL)
                        THEN true ELSE false END AS invalid
            """
        )
        node_ids = {str(row["id"]) for row in rows if row.get("id")}
        return (
            node_ids,
            {
                "orphan_nodes": sum(1 for row in rows if row.get("orphan")),
                "invalid_nodes": sum(1 for row in rows if row.get("invalid")),
            },
            None,
        )
    except Exception as error:
        return set(), {"orphan_nodes": 0, "invalid_nodes": 0}, str(error)


def embedding_snapshot() -> tuple[set[str], str | None]:
    try:
        from dkg_api.app.db.qdrant_client import COLLECTION_NAME, QdrantClient

        client = QdrantClient().client
        next_page = None
        node_ids = set()
        while True:
            points, next_page = client.scroll(
                collection_name=COLLECTION_NAME,
                limit=100,
                offset=next_page,
                with_payload=True,
            )
            for point in points:
                payload = point.payload or {}
                node_id = payload.get("node_id")
                if node_id:
                    node_ids.add(str(node_id))
            if next_page is None:
                break
        return node_ids, None
    except Exception as error:
        return set(), str(error)


def risk_for(
    orphan_nodes: int,
    embedding_mismatch: int,
    invalid_nodes: int,
    graph_error: str | None,
    embedding_error: str | None,
) -> str:
    if graph_error or embedding_error or invalid_nodes > 0:
        return "high"
    if orphan_nodes > 0 or embedding_mismatch > 0:
        return "medium"
    return "low"


def main() -> int:
    payload = collect()
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["risk_level"] in {"low", "medium"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
