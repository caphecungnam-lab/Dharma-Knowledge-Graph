from __future__ import annotations

import unittest
from pathlib import Path

from dkg_api.app.safety.context_sanitizer import ContextSanitizer
from dkg_api.app.safety.output_validator import OutputValidator
from dkg_api.app.safety.retrieval_control_layer import RetrievalControlLayer


ROOT = Path(__file__).resolve().parents[1]


class SafetyGuardsTest(unittest.TestCase):
    def test_ai_route_uses_retrieval_control_layer_instead_of_raw_search(self):
        ai_source = (ROOT / "dkg_api/app/api/ai.py").read_text()
        safety_source = (
            ROOT / "dkg_api/app/safety/safety_orchestrator.py"
        ).read_text()

        self.assertIn("AIOrchestrator", ai_source)
        self.assertNotIn("RetrievalControlLayer", ai_source)
        self.assertIn("RetrievalControlLayer", safety_source)
        self.assertIn("self.retrieval.fetch", safety_source)
        self.assertNotIn("vector.search(", ai_source)
        self.assertNotIn("graph.related_concepts(", ai_source)

    def test_context_sanitizer_removes_fake_unsafe_node(self):
        unsafe_node = {
            "node_id": "fake_node",
            "confidence": 0.1,
            "epistemic_type": "unknown",
            "ai_usage_allowed": False,
            "traceability": {"node_id": "fake_node", "sources": [], "graph_links": []},
            "match": {"tradition": "theravada"},
        }

        sanitized = ContextSanitizer().sanitize(
            [unsafe_node],
            allowed_layers=["core_fact", "doctrinal", "interpretive", "esoteric"],
        )

        self.assertEqual(sanitized, [])

    def test_output_validator_blocks_unsafe_output(self):
        validation = OutputValidator().validate(
            {
                "answer": "This invents untraceable doctrine.",
                "confidence": 0.95,
                "used_nodes": ["fake_node"],
            },
            [],
        )

        self.assertEqual(validation["status"], "REJECTED")
        self.assertIn("missing_context", validation["errors"])

    def test_retrieval_control_layer_is_mandatory_for_untrusted_nodes(self):
        class FakeVector:
            def search(self, query):
                return [
                    {
                        "node_id": "fake_node",
                        "confidence": 0.1,
                        "epistemic_type": "unknown",
                        "score": 0.1,
                        "text": "Unsafe.",
                    }
                ]

        class FakeGraph:
            def related_concepts(self, node_id):
                return []

        result = RetrievalControlLayer().fetch("unsafe", FakeVector(), FakeGraph())

        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
