from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from dkg_api.app.ingestion.corpus_loader import CorpusLoader
from dkg_api.app.ingestion.entity_normalizer import EntityNormalizer
from dkg_api.app.ingestion.ingestion_pipeline import IngestionPipeline
from dkg_api.app.ingestion.knowledge_extractor import KnowledgeExtractor
from dkg_api.app.ingestion.text_chunker import TextChunker


class FakeVectorClient:
    def __init__(self) -> None:
        self.points = []

    def upsert_points(self, points):
        self.points.extend(points)


class FakeVectorService:
    def __init__(self) -> None:
        self.client = FakeVectorClient()


class FakeGraphService:
    def __init__(self) -> None:
        self.nodes = []
        self.chunks = []
        self.relationships = []
        self.contradictions = []

    def upsert_generated_node(self, node):
        self.nodes.append(node)

    def link_source_chunk(self, node):
        self.chunks.append(node)

    def create_relationship(self, source_id, target_id, relationship_type):
        self.relationships.append(
            {
                "source": source_id,
                "target": target_id,
                "type": relationship_type,
            }
        )

    def create_contradiction(self, contradiction):
        self.contradictions.append(contradiction)


class CorpusIngestionPipelineTest(unittest.TestCase):
    def write_temp_text(self, text: str) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "source.txt"
        path.write_text(text, encoding="utf-8")
        return path

    def metadata(self):
        return {
            "source_id": "source_test_001",
            "tradition": "theravada",
            "author": "Test Author",
            "title": "Test Source",
            "source_type": "sutta",
        }

    def test_corpus_loader_loads_txt_with_metadata(self):
        path = self.write_temp_text("Impermanence is related to suffering.")

        doc = CorpusLoader().load(path, self.metadata())

        self.assertEqual(doc["source_metadata"]["source_id"], "source_test_001")
        self.assertIn("Impermanence", doc["text"])

    def test_text_chunker_preserves_sentence_boundaries(self):
        chunks = TextChunker(max_tokens=50).chunk(
            "Impermanence is taught. Suffering is taught.",
            source_id="source_test_001",
        )

        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["chunk_id"], "source_test_001_chunk_0001")
        self.assertIn("Suffering is taught.", chunks[0]["text"])

    def test_knowledge_extractor_only_extracts_explicit_concepts(self):
        chunk = {
            "chunk_id": "chunk_001",
            "text": "Impermanence is related to suffering.",
            "position": 0,
        }

        extracted = KnowledgeExtractor().extract(chunk, self.metadata())

        labels = {concept["canonical_label"] for concept in extracted["concepts"]}
        self.assertEqual(labels, {"impermanence", "suffering"})
        self.assertEqual(extracted["relations"][0]["type"], "RELATED_TO")

    def test_entity_normalizer_unifies_synonyms(self):
        extracted = {
            "concepts": [
                {
                    "label": "anicca",
                    "definition": "Anicca is taught.",
                }
            ],
            "relations": [],
            "statements": [],
        }

        normalized = EntityNormalizer().normalize(extracted)

        self.assertEqual(normalized["concepts"][0]["label"], "impermanence")
        self.assertEqual(normalized["concepts"][0]["id"], "concept_impermanence")

    def test_ingestion_pipeline_stores_only_validated_nodes(self):
        path = self.write_temp_text(
            "Impermanence is related to suffering. Karma is mentioned in the same source."
        )
        graph = FakeGraphService()
        vector = FakeVectorService()

        result = IngestionPipeline(graph, vector).run(path, self.metadata())

        self.assertEqual(result["status"], "ok")
        self.assertGreaterEqual(result["validated_nodes"], 2)
        self.assertGreaterEqual(len(vector.client.points), 1)
        self.assertTrue(all(node.get("ai_usage_allowed") is True for node in graph.nodes))
        self.assertTrue(all(node["traceability"]["sources"] for node in graph.nodes))

    def test_ingestion_pipeline_rejects_uncertain_chunks(self):
        path = self.write_temp_text("This paragraph has no known Buddhist concept keyword.")
        graph = FakeGraphService()
        vector = FakeVectorService()

        result = IngestionPipeline(graph, vector).run(path, self.metadata())

        self.assertEqual(result["status"], "rejected")
        self.assertEqual(result["rejections"][0]["reason"], "epistemic_uncertainty")
        self.assertEqual(graph.nodes, [])


if __name__ == "__main__":
    unittest.main()
