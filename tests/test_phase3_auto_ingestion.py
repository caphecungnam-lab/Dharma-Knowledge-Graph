from __future__ import annotations

import unittest

from dkg_api.app.services.auto_ingestion_engine import AutoIngestionEngine
from dkg_api.app.services.contradiction_miner import ContradictionMiner
from dkg_api.app.services.knowledge_extractor import KnowledgeExtractor
from dkg_api.app.services.tradition_mapper import TraditionMapper


class FakeGraphService:
    def __init__(self) -> None:
        self.nodes = []
        self.source_links = []
        self.relationships = []
        self.contradictions = []

    def upsert_generated_node(self, node):
        self.nodes.append(node)

    def link_source_chunk(self, node):
        self.source_links.append(node)

    def create_relationship(self, source_id, target_id, relationship_type):
        self.relationships.append((source_id, target_id, relationship_type))

    def create_contradiction(self, contradiction):
        self.contradictions.append(contradiction)


class Phase3AutoIngestionTest(unittest.TestCase):
    def test_extractor_creates_traceable_candidates(self) -> None:
        extractor = KnowledgeExtractor()
        chunks = extractor.split_into_chunks(
            "Impermanence and suffering are related to meditation."
        )

        extracted = extractor.extract_candidates(
            chunks,
            {"source_id": "source_001", "source_type": "sutta"},
        )

        node_ids = {node["node_id"] for node in extracted["nodes"]}
        self.assertIn("concept_impermanence", node_ids)
        self.assertIn("concept_suffering", node_ids)
        self.assertIn("practice_meditation", node_ids)
        self.assertTrue(
            all(node["source_id"] == "source_001" for node in extracted["nodes"])
        )

    def test_contradiction_miner_classifies_death_bardo(self) -> None:
        miner = ContradictionMiner()
        contradictions = miner.mine(
            [
                {
                    "label": "death",
                    "tradition": "theravada",
                    "text": "Death is dissolution of aggregates.",
                },
                {
                    "label": "death",
                    "tradition": "vajrayana",
                    "text": "Death is transition into bardo consciousness.",
                },
            ]
        )

        self.assertEqual(contradictions[0]["conflict_type"], "doctrinal")
        self.assertEqual(contradictions[0]["severity"], 0.7)

    def test_tradition_mapper_marks_shared_core(self) -> None:
        mapper = TraditionMapper()

        tradition = mapper.map_tradition(
            "Theravada Mahayana Vajrayana all discuss impermanence."
        )

        self.assertEqual(tradition, "shared_core")

    def test_auto_ingestion_validates_before_graph_insert(self) -> None:
        graph = FakeGraphService()
        engine = AutoIngestionEngine(graph)

        result = engine.process_text(
            "Impermanence and suffering are taught in this sutta.",
            {"source_id": "source_001", "source_type": "sutta"},
        )

        self.assertGreaterEqual(len(result["validated_nodes"]), 2)
        self.assertEqual(len(graph.nodes), len(result["validated_nodes"]))
        self.assertTrue(graph.source_links)


if __name__ == "__main__":
    unittest.main()
