from __future__ import annotations

import unittest

from dkg_api.app.safety.context_sanitizer import ContextSanitizer
from dkg_api.app.safety.epistemic_gateway import EpistemicGateway
from dkg_api.app.safety.output_validator import OutputValidator
from dkg_api.app.safety.retrieval_control_layer import RetrievalControlLayer
from dkg_api.app.services.ai_reasoner import AIReasoner
from dkg_api.app.services.epistemic_truth_system import EpistemicTruthSystem


class InMemoryVector:
    def __init__(self) -> None:
        self.nodes = []

    def ingest(self, concept):
        self.nodes.append(
            {
                "node_id": concept["id"],
                "text": concept["definition"],
                "tradition": concept["tradition"],
                "source_id": concept["source_id"],
                "source_type": concept["source_type"],
                "score": 0.92,
            }
        )

    def search(self, query):
        return [
            node for node in self.nodes if "death" in node["text"].lower()
        ]


class InMemoryGraph:
    def __init__(self) -> None:
        self.related = {}

    def ingest(self, concept):
        self.related[concept["id"]] = []

    def related_concepts(self, node_id):
        return self.related.get(node_id, [])


class E2EPipelineTest(unittest.TestCase):
    def test_death_query_passes_full_safety_pipeline(self):
        concept = {
            "id": "concept_death",
            "label": "death",
            "definition": "Death is the ending of a life process in conditioned existence.",
            "tradition": "theravada",
            "source_id": "source_seed_death_001",
            "source_type": "sutta",
        }
        vector = InMemoryVector()
        graph = InMemoryGraph()
        vector.ingest(concept)
        graph.ingest(concept)
        query = "What does Buddhism say about death?"

        gateway = EpistemicGateway()
        classification = gateway.classify_query(query)
        retrieved = RetrievalControlLayer().fetch(query, vector, graph)
        evaluated = EpistemicTruthSystem().evaluate(retrieved)
        sanitized = ContextSanitizer().sanitize(
            EpistemicTruthSystem().filter_ai_usable(evaluated),
            allowed_layers=classification["allowed_layers"],
        )
        answer = AIReasoner().generate(query, sanitized)
        validation = OutputValidator().validate(answer, sanitized)

        self.assertEqual(classification["mode"], "core_fact")
        self.assertEqual(retrieved[0]["match"]["node_id"], "concept_death")
        self.assertEqual(sanitized[0]["node_id"], "concept_death")
        self.assertEqual(sanitized[0]["source_ids"], ["source_seed_death_001"])
        self.assertEqual(validation["status"], "APPROVED")
        self.assertEqual(answer["used_nodes"], ["concept_death"])
        self.assertEqual(answer["used_sources"], ["source_seed_death_001"])
        self.assertNotIn("bardo", answer["answer"].lower())


if __name__ == "__main__":
    unittest.main()
