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

    def upsert_generated_node(self, node: dict[str, Any]) -> None:
        match = node.get("match", {})
        payload = {
            "id": node["node_id"],
            "label": match.get("label") or node["node_id"],
            "definition": match.get("definition") or match.get("text") or "",
            "tradition": match.get("tradition") or "shared_core",
            "epistemic_type": node.get("epistemic_type"),
            "confidence": node.get("confidence"),
            "source_id": (node.get("traceability") or {}).get("sources", [""])[0],
        }

        if match.get("node_type") == "Practice":
            self.client.execute_write(
                """
                MERGE (n:Practice {id: $id})
                ON CREATE SET
                    n.label = $label,
                    n.definition = $definition,
                    n.tradition = $tradition
                SET n.epistemic_type = coalesce(n.epistemic_type, $epistemic_type),
                    n.last_confidence = $confidence,
                    n.last_source_id = $source_id
                RETURN n
                """,
                **payload,
            )
            return

        self.client.execute_write(
            """
            MERGE (n:Concept {id: $id})
            ON CREATE SET
                n.label = $label,
                n.definition = $definition,
                n.tradition = $tradition
            SET n.epistemic_type = coalesce(n.epistemic_type, $epistemic_type),
                n.last_confidence = $confidence,
                n.last_source_id = $source_id
            RETURN n
            """,
            **payload,
        )

    def link_source_chunk(self, node: dict[str, Any]) -> None:
        match = node.get("match", {})
        traceability = node.get("traceability") or {}
        source_id = str((traceability.get("sources") or ["source_text"])[0])
        chunk_id = str(match.get("chunk_id") or f"{source_id}_chunk")
        chunk_text = str(match.get("text") or "")
        node_id = str(node.get("node_id") or "")

        self.client.execute_write(
            """
            MERGE (chunk:SourceChunk {id: $chunk_id})
            ON CREATE SET
                chunk.source_id = $source_id,
                chunk.text = $chunk_text
            WITH chunk
            MATCH (n {id: $node_id})
            MERGE (n)-[:SUPPORTED_BY]->(chunk)
            RETURN chunk
            """,
            chunk_id=chunk_id,
            source_id=source_id,
            chunk_text=chunk_text,
            node_id=node_id,
        )

    def create_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship_type: str,
    ) -> None:
        safe_type = (
            relationship_type if relationship_type.isidentifier() else "RELATED_TO"
        )
        query = f"""
        MATCH (source {{id: $source_id}})
        MATCH (target {{id: $target_id}})
        MERGE (source)-[:{safe_type}]->(target)
        RETURN source, target
        """
        self.client.execute_write(query, source_id=source_id, target_id=target_id)

    def create_contradiction(self, contradiction: dict[str, object]) -> None:
        contradiction_id = (
            f"{contradiction.get('concept')}:"
            f"{contradiction.get('tradition_a')}:"
            f"{contradiction.get('tradition_b')}:"
            f"{contradiction.get('conflict_type')}"
        )
        self.client.execute_write(
            """
            MERGE (c:Contradiction {id: $id})
            SET c.concept = $concept,
                c.conflict_type = $conflict_type,
                c.tradition_a = $tradition_a,
                c.tradition_b = $tradition_b,
                c.severity = $severity
            RETURN c
            """,
            id=contradiction_id,
            **contradiction,
        )

    def expand_node(self, node_id: str) -> dict[str, Any]:
        related = self.related_concepts(node_id)
        return {
            "node_id": node_id,
            "related": related,
        }

    def contradictions(self) -> list[dict[str, Any]]:
        rows = self.client.execute_read("""
            MATCH (c:Contradiction)
            RETURN c {
                .concept,
                .conflict_type,
                .tradition_a,
                .tradition_b,
                .severity
            } AS contradiction
            ORDER BY c.concept
            """)
        return [row["contradiction"] for row in rows]

    def evolution(self) -> dict[str, Any]:
        rows = self.client.execute_read("""
            MATCH (n)
            WHERE n:Concept OR n:Practice
            RETURN labels(n) AS labels, count(n) AS count
            ORDER BY labels(n)
            """)
        return {
            "node_counts": rows,
        }
