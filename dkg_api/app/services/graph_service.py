from __future__ import annotations

from typing import Any

from dkg_api.app.db.neo4j_client import Neo4jClient


class GraphService:
    def __init__(self, client: Neo4jClient) -> None:
        self.client = client

    def upsert_concept(self, concept: dict[str, str]) -> None:
        self.client.execute_write(
            """
            MERGE (c:Concept {id: $id})
            SET c.label = $label,
                c.definition = $definition,
                c.tradition = $tradition
            RETURN c
            """,
            **concept,
        )

    def related_concepts(self, node_id: str) -> list[dict[str, Any]]:
        rows = self.client.execute_read(
            """
            MATCH (:Concept {id: $id})-[:RELATED_TO]-(related:Concept)
            RETURN related {
                .id,
                .label,
                .definition,
                .tradition
            } AS concept
            LIMIT 10
            """,
            id=node_id,
        )
        return [row["concept"] for row in rows]
