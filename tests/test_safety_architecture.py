from __future__ import annotations

import unittest

from dkg_api.app.safety.context_sanitizer import ContextSanitizer
from dkg_api.app.safety.epistemic_gateway import EpistemicGateway
from dkg_api.app.safety.output_validator import OutputValidator
from dkg_api.app.safety.retrieval_control_layer import RetrievalControlLayer
from dkg_api.app.safety.safety_policy import SafetyPolicy
from dkg_api.app.services.ai_reasoner import AIReasoner


class FakeVector:
    def __init__(self, matches):
        self.matches = matches

    def search(self, query):
        return self.matches


class FakeGraph:
    def related_concepts(self, node_id):
        return [{"id": "related_dukkha", "tradition": "theravada"}]


class SafetyArchitectureTest(unittest.TestCase):
    def valid_context(self):
        return [
            {
                "node_id": "concept_dukkha",
                "epistemic_type": "core_fact",
                "confidence": 0.95,
                "tradition": "theravada",
                "ai_usage_allowed": True,
                "conflict": {"type": "none", "severity": 0.0},
                "traceability": {
                    "node_id": "concept_dukkha",
                    "sources": ["source_sutta_001"],
                    "graph_links": [],
                },
                "match": {
                    "node_id": "concept_dukkha",
                    "text": "Dukkha means unsatisfactoriness.",
                    "tradition": "theravada",
                },
            }
        ]

    def test_gateway_classifies_core_comparative_esoteric_and_reject(self):
        gateway = EpistemicGateway()

        self.assertEqual(gateway.classify_query("What is dukkha?")["mode"], "core_fact")
        self.assertEqual(
            gateway.classify_query("Compare Theravada and Mahayana")["mode"],
            "multi_tradition",
        )
        self.assertEqual(gateway.classify_query("What is bardo?")["mode"], "esoteric")
        self.assertEqual(gateway.classify_query("Invent a doctrine")["mode"], "reject")

    def test_retrieval_control_rejects_untraceable_and_low_confidence_nodes(self):
        matches = [
            {"node_id": "a", "score": 0.9, "text": "No source."},
            {
                "node_id": "b",
                "score": 0.4,
                "text": "Too weak.",
                "source_id": "source_001",
            },
            {
                "node_id": "c",
                "score": 0.9,
                "text": "Traceable.",
                "source_id": "source_002",
            },
        ]

        result = RetrievalControlLayer().fetch("dukkha", FakeVector(matches), FakeGraph())

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["match"]["node_id"], "c")

    def test_context_sanitizer_keeps_only_allowed_traceable_context(self):
        context = self.valid_context() + [
            {
                "node_id": "unknown",
                "epistemic_type": "unknown",
                "confidence": 0.2,
                "ai_usage_allowed": False,
                "traceability": {"node_id": "", "sources": [], "graph_links": []},
            },
            {
                "node_id": "vajrayana_only",
                "epistemic_type": "esoteric_view",
                "confidence": 0.8,
                "ai_usage_allowed": True,
                "traceability": {
                    "node_id": "vajrayana_only",
                    "sources": ["source_tantra_001"],
                    "graph_links": [],
                },
            },
        ]

        result = ContextSanitizer().sanitize(context, allowed_layers=["core_fact"])

        self.assertEqual([node["node_id"] for node in result], ["concept_dukkha"])

    def test_output_validator_approves_traceable_reasoner_output(self):
        context = self.valid_context()
        answer = AIReasoner().generate("What is dukkha?", context)

        validation = OutputValidator().validate(answer, context)

        self.assertEqual(validation["status"], "APPROVED")
        self.assertEqual(validation["errors"], [])
        self.assertEqual(answer["used_sources"], ["source_sutta_001"])
        self.assertEqual(answer["epistemic_types"], ["core_fact"])

    def test_output_validator_rejects_incorrect_tradition_merge(self):
        context = self.valid_context() + [
            {
                **self.valid_context()[0],
                "node_id": "concept_bardo",
                "epistemic_type": "esoteric_view",
                "tradition": "vajrayana",
                "conflict": {"type": "doctrinal", "severity": 0.7},
                "traceability": {
                    "node_id": "concept_bardo",
                    "sources": ["source_tantra_001"],
                    "graph_links": [],
                },
            }
        ]
        answer = {
            "answer": "All traditions agree that death means bardo.",
            "confidence": 0.9,
            "used_nodes": ["concept_dukkha", "concept_bardo"],
        }

        validation = OutputValidator().validate(answer, context)

        self.assertEqual(validation["status"], "REJECTED")
        self.assertIn("incorrect_tradition_merge", validation["errors"])

    def test_safety_policy_tone_rules(self):
        policy = SafetyPolicy()

        self.assertEqual(policy.apply_tone_rules(0.95), "assertive")
        self.assertEqual(policy.apply_tone_rules(0.75), "academic")
        self.assertEqual(policy.apply_tone_rules(0.55), "interpretive")
        self.assertEqual(policy.apply_tone_rules(0.2), "refuse")


if __name__ == "__main__":
    unittest.main()
