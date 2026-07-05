from __future__ import annotations

import json


def collect() -> dict[str, object]:
    try:
        from dkg_api.app.db.neo4j_client import Neo4jClient

        client = Neo4jClient()
        total_nodes = client.execute_read("MATCH (n) RETURN count(n) AS count")[0]["count"]
        orphan_nodes = client.execute_read(
            "MATCH (n) WHERE NOT (n)--() RETURN count(n) AS count"
        )[0]["count"]
        invalid_nodes = client.execute_read(
            """
            MATCH (n)
            WHERE (n:Concept OR n:Practice)
              AND (n.source_id IS NULL AND n.last_source_id IS NULL)
            RETURN count(n) AS count
            """
        )[0]["count"]
        duplicate_rows = client.execute_read(
            """
            MATCH (c:Concept)
            WITH toLower(c.label) AS label, count(c) AS count
            WHERE label IS NOT NULL AND count > 1
            RETURN sum(count - 1) AS duplicates
            """
        )
        duplicates = duplicate_rows[0].get("duplicates") or 0
        cluster_rows = client.execute_read(
            """
            MATCH (n)
            WITH collect(n) AS nodes
            UNWIND nodes AS start
            MATCH path=(start)-[*0..3]-(neighbor)
            WITH start, collect(DISTINCT neighbor) AS component
            RETURN count(DISTINCT component) AS clusters
            """
        )
        cluster_count = cluster_rows[0].get("clusters") or 0
        return {
            "total_nodes": total_nodes,
            "orphan_nodes": orphan_nodes,
            "invalid_nodes": invalid_nodes,
            "duplicate_concepts": duplicates,
            "cluster_count": cluster_count,
            "status": "ok",
        }
    except Exception as error:
        return {
            "total_nodes": 0,
            "orphan_nodes": 0,
            "invalid_nodes": 0,
            "duplicate_concepts": 0,
            "cluster_count": 0,
            "status": "fail",
            "error": str(error),
        }


def main() -> int:
    payload = collect()
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
