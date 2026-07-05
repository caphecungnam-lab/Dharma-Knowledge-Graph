from __future__ import annotations

import unittest

from dkg_api.app.cache.query_cache import QueryCache
from dkg_api.app.observability.metrics import MetricsCollector
from dkg_api.app.safety.retrieval_control_layer import RetrievalControlLayer
from dkg_api.app.services.context_reduction_engine import ContextReductionEngine


class FakeVectorFailure:
    def search(self, query):
        raise RuntimeError("qdrant unavailable")


class FakeGraphSearch:
    def search_concepts(self, query):
        return [
            {
                "node_id": "concept_death",
                "text": "Death is discussed in a traceable source.",
                "tradition": "theravada",
                "source_id": "source_001",
                "score": 0.8,
            }
        ]


class FakeVectorSearch:
    def search(self, query):
        return [
            {
                "node_id": "concept_death",
                "text": "Death is discussed in a traceable source.",
                "tradition": "theravada",
                "source_id": "source_001",
                "score": 0.8,
            }
        ]


class FakeGraphFailure:
    def related_concepts(self, node_id):
        raise RuntimeError("neo4j unavailable")


class RuntimeHardeningTest(unittest.TestCase):
    def test_query_cache_tracks_hits_and_misses(self):
        cache = QueryCache(max_size=2)

        self.assertIsNone(cache.get("dukkha"))
        cache.set("dukkha", {"answer": "traceable"}, ttl_seconds=30)
        self.assertEqual(cache.get("dukkha"), {"answer": "traceable"})

        stats = cache.stats()
        self.assertEqual(stats["hits"], 1)
        self.assertEqual(stats["misses"], 1)
        self.assertEqual(stats["hit_rate"], 0.5)

    def test_query_cache_uses_short_ttl_for_interpretive_context(self):
        cache = QueryCache()

        ttl = cache.ttl_for_context([{"epistemic_type": "interpretive"}])

        self.assertEqual(ttl, 120)

    def test_context_reduction_prioritizes_core_fact_and_confidence(self):
        context = [
            {
                "node_id": "interpretive",
                "epistemic_type": "interpretive",
                "confidence": 0.95,
                "match": {"text": "Interpretive view."},
                "related": [1, 2, 3, 4],
            },
            {
                "node_id": "core",
                "epistemic_type": "core_fact",
                "confidence": 0.7,
                "match": {"text": "Core fact."},
                "related": [1, 2, 3, 4],
            },
        ]

        reduced = ContextReductionEngine().reduce(context, max_nodes=2)

        self.assertEqual(reduced[0]["node_id"], "core")
        self.assertEqual(len(reduced[0]["related"]), 3)

    def test_retrieval_control_falls_back_to_graph_when_vector_fails(self):
        result = RetrievalControlLayer().fetch(
            "death",
            FakeVectorFailure(),
            FakeGraphSearch(),
        )

        self.assertEqual(result[0]["match"]["node_id"], "concept_death")

    def test_retrieval_control_uses_vector_only_when_graph_fails(self):
        result = RetrievalControlLayer().fetch(
            "death",
            FakeVectorSearch(),
            FakeGraphFailure(),
        )

        self.assertEqual(result[0]["related"], [])
        self.assertEqual(result[0]["match"]["node_id"], "concept_death")

    def test_metrics_tracks_truth_rejection_rate(self):
        collector = MetricsCollector()

        collector.record_truth_filtering(evaluated_count=10, sanitized_count=6)

        self.assertEqual(collector.health_metrics()["truth_rejection_rate"], 0.4)


if __name__ == "__main__":
    unittest.main()
