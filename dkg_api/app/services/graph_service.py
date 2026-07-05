from __future__ import annotations

from typing import Any

from dkg_api.app.cache.graph_cache import graph_cache
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
                c.tradition = $tradition,
                c.source_id = $source_id,
                c.source_type = $source_type,
                c.epistemic_type = coalesce(c.epistemic_type, "core_fact"),
                c.last_confidence = coalesce(c.last_confidence, 0.9)
            RETURN c
            """,
            id=concept["id"],
            label=concept["label"],
            definition=concept["definition"],
            tradition=concept["tradition"],
            source_id=concept.get("source_id") or "seed_data",
            source_type=concept.get("source_type") or "seed_data",
        )

    def related_concepts(self, node_id: str) -> list[dict[str, Any]]:
        cache_key = f"related:{node_id}"
        cached = graph_cache.get(cache_key)
        if cached is not None:
            return cached

        rows = self.client.execute_read(
            """
            MATCH (:Concept {id: $id})-[:RELATED_TO]-(related:Concept)
            RETURN related {
                .id,
                .label,
                .definition,
                .tradition,
                source_id: coalesce(related.source_id, related.last_source_id),
                .source_type
            } AS concept
            LIMIT 10
            """,
            id=node_id,
        )
        concepts = [row["concept"] for row in rows]
        graph_cache.set(cache_key, concepts, ttl_seconds=300)
        return concepts

    def search_concepts(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        rows = self.client.execute_read(
            """
            MATCH (c:Concept)
            WHERE toLower(c.label) CONTAINS toLower($query)
               OR toLower(c.definition) CONTAINS toLower($query)
            RETURN c {
                node_id: c.id,
                text: c.definition,
                .tradition,
                source_id: coalesce(c.source_id, c.last_source_id),
                .source_type,
                score: coalesce(c.last_confidence, 0.6)
            } AS concept
            LIMIT $limit
            """,
            query=query,
            limit=limit,
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

    def visualization_neighborhood(self, concept_id: str) -> dict[str, Any]:
        nodes = self.client.execute_read(
            """
            MATCH (center {id: $concept_id})
            RETURN center {
                .id,
                .label,
                .definition,
                .tradition,
                .epistemic_type,
                source_id: coalesce(center.source_id, center.last_source_id),
                .source_type,
                confidence: coalesce(center.last_confidence, 0.5)
            } AS node
            UNION
            MATCH ({id: $concept_id})-[r]-(neighbor)
            WHERE neighbor:Concept OR neighbor:Practice
            RETURN neighbor {
                .id,
                .label,
                .definition,
                .tradition,
                .epistemic_type,
                source_id: coalesce(neighbor.source_id, neighbor.last_source_id),
                .source_type,
                confidence: coalesce(neighbor.last_confidence, 0.5)
            } AS node
            LIMIT 50
            """,
            concept_id=concept_id,
        )
        edges = self.client.execute_read(
            """
            MATCH (source {id: $concept_id})-[r]-(target)
            WHERE target:Concept OR target:Practice
            RETURN {
                from: source.id,
                to: target.id,
                type: type(r),
                strength: coalesce(r.confidence, target.last_confidence, 0.7)
            } AS edge
            LIMIT 80
            """,
            concept_id=concept_id,
        )
        contradictions = self.client.execute_read(
            """
            MATCH (c:Contradiction {concept: $concept_id})
            RETURN {
                from: c.tradition_a,
                to: c.tradition_b,
                type: toUpper(c.conflict_type) + "_CONFLICT",
                strength: c.severity
            } AS edge
            """,
            concept_id=concept_id,
        )
        return {
            "nodes": [row["node"] for row in nodes],
            "edges": [row["edge"] for row in edges]
            + [row["edge"] for row in contradictions],
        }

    def path_between(self, source_id: str, target_id: str) -> list[dict[str, Any]]:
        rows = self.client.execute_read(
            """
            MATCH path = shortestPath((source {id: $source_id})-[*..6]-(target {id: $target_id}))
            WITH relationships(path) AS rels
            UNWIND rels AS rel
            WITH startNode(rel) AS source, endNode(rel) AS target, rel
            RETURN {
                from: source.id,
                to: target.id,
                type: type(rel),
                confidence: coalesce(rel.confidence, target.last_confidence, 0.5),
                tradition: coalesce(target.tradition, source.tradition, "shared_core")
            } AS step
            """,
            source_id=source_id,
            target_id=target_id,
        )
        return [row["step"] for row in rows]
