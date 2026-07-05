from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Any

from dkg_api.app.db.graph_write_guard import GraphWriteGuard
from dkg_api.app.ingestion.deduplication_engine import DeduplicationEngine
from dkg_api.app.ingestion.ingestion_pipeline import IngestionPipeline
from dkg_api.app.ingestion.validation_layer import validate_ingested_node


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


class LowConfidenceExtractor:
    def extract(self, chunk: dict[str, Any], source_metadata: dict[str, Any]):
        return {
            "concepts": [
                {
                    "id": "concept_karma",
                    "label": "karma",
                    "canonical_label": "karma",
                    "definition": "Karma appears in this source.",
                    "source_id": source_metadata["source_id"],
                    "source_type": source_metadata["source_type"],
                    "tradition": source_metadata["tradition"],
                    "chunk_id": chunk["chunk_id"],
                    "position": chunk["position"],
                    "score": 0.1,
                }
            ],
            "relations": [],
            "statements": [],
        }


class ConflictingExtractor:
    def extract(self, chunk: dict[str, Any], source_metadata: dict[str, Any]):
        return {
            "concepts": [
                {
                    "id": "concept_death_a",
                    "label": "death",
                    "canonical_label": "death",
                    "definition": "Death is described one way.",
                    "source_id": source_metadata["source_id"],
                    "source_type": source_metadata["source_type"],
                    "tradition": "theravada",
                    "chunk_id": chunk["chunk_id"],
                    "position": chunk["position"],
                },
                {
                    "id": "concept_death_b",
                    "label": "death",
                    "canonical_label": "death",
                    "definition": "Death is described differently.",
                    "source_id": source_metadata["source_id"],
                    "source_type": source_metadata["source_type"],
                    "tradition": "vajrayana",
                    "chunk_id": chunk["chunk_id"],
                    "position": chunk["position"],
                },
            ],
            "relations": [],
            "statements": [],
        }


class MalformedChunker:
    def chunk(self, text: str, source_id: str = "source"):
        return [{"chunk_id": "bad_chunk", "text": "", "position": 0}]


class Day2IngestionTest(unittest.TestCase):
    def write_temp_text(self, text: str) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "source.txt"
        path.write_text(text, encoding="utf-8")
        return path

    def metadata(self):
        return {
            "source_id": "source_day2_001",
            "tradition": "theravada",
            "author": "Test Author",
            "title": "Day 2 Test",
            "source_type": "sutta",
        }

    def test_valid_buddhist_concept_ingestion(self):
        path = self.write_temp_text("Impermanence is related to suffering.")
        graph = FakeGraphService()
        vector = FakeVectorService()

        result = IngestionPipeline(graph, vector).run(path, self.metadata())

        self.assertEqual(result["status"], "ok")
        self.assertGreaterEqual(len(graph.nodes), 2)
        self.assertTrue(all(node["traceability"]["sources"] for node in graph.nodes))
        self.assertTrue(all((node["match"] or {}).get("chunk_id") for node in graph.nodes))

    def test_missing_source_id_must_fail(self):
        node = {
            "node_id": "concept_karma",
            "epistemic_type": "core_fact",
            "confidence": 0.9,
            "match": {
                "node_id": "concept_karma",
                "label": "karma",
                "definition": "Karma is intentional action.",
                "tradition": "theravada",
                "chunk_id": "chunk_001",
            },
        }

        result = validate_ingested_node(node)

        self.assertEqual(result["status"], "rejected")
        self.assertEqual(result["reason"], "missing_source")

    def test_low_confidence_extraction_must_reject(self):
        path = self.write_temp_text("Karma appears in this source.")
        graph = FakeGraphService()
        vector = FakeVectorService()

        result = IngestionPipeline(
            graph,
            vector,
            extractor=LowConfidenceExtractor(),
        ).run(path, self.metadata())

        self.assertEqual(result["status"], "rejected")
        self.assertEqual(result["rejections"][0]["stage"], "validate")
        self.assertEqual(result["rejections"][0]["reason"], "low_confidence")
        self.assertEqual(graph.nodes, [])

    def test_conflicting_doctrine_input_flags_not_merge(self):
        report = DeduplicationEngine().analyze(
            [
                {
                    "label": "death",
                    "definition": "Death is described one way.",
                    "tradition": "theravada",
                },
                {
                    "label": "death",
                    "definition": "Death is described differently.",
                    "tradition": "vajrayana",
                },
            ]
        )

        self.assertEqual(report["conflicts"][0]["type"], "conflicting_definitions")
        self.assertEqual(report["merged_suggestions"], [])

    def test_malformed_chunk_must_stop_pipeline(self):
        path = self.write_temp_text("Impermanence is taught.")
        graph = FakeGraphService()
        vector = FakeVectorService()

        result = IngestionPipeline(
            graph,
            vector,
            chunker=MalformedChunker(),
        ).run(path, self.metadata())

        self.assertEqual(result["status"], "rejected")
        self.assertEqual(result["stage"], "chunk")
        self.assertEqual(graph.nodes, [])

    def test_graph_write_guard_blocks_unknown_epistemic_type(self):
        guard = GraphWriteGuard(FakeGraphService())
        node = {
            "node_id": "concept_fake",
            "epistemic_type": "unknown",
            "confidence": 0.9,
            "match": {
                "node_id": "concept_fake",
                "label": "fake",
                "definition": "Fake doctrine.",
                "tradition": "theravada",
                "source_id": "source_fake",
                "chunk_id": "chunk_fake",
            },
        }

        result = guard.write_node(node)

        self.assertEqual(result["status"], "rejected")
        self.assertEqual(result["stage"], "graph_write")


if __name__ == "__main__":
    unittest.main()
