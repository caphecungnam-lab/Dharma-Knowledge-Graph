from __future__ import annotations

import unittest

from dkg_api.app.services.adaptive_explainer import AdaptiveExplainer
from dkg_api.app.services.dharma_path_engine import DharmaPathEngine
from dkg_api.app.services.learning_state_tracker import LearningStateTracker
from dkg_api.app.services.progression_mapper import ProgressionMapper
from dkg_api.app.services.user_epistemic_model import UserEpistemicModel


class Phase5LearningIntelligenceTest(unittest.TestCase):
    def validated_context(self):
        return [
            {
                "node_id": "impermanence",
                "epistemic_type": "core_fact",
                "confidence": 0.9,
                "tradition": "theravada",
                "ai_usage_allowed": True,
                "conflict": {"type": "none", "severity": 0.0},
                "match": {
                    "label": "impermanence",
                    "definition": "All conditioned phenomena are unstable.",
                },
            }
        ]

    def test_user_profile_defaults_to_epistemic_tracking(self):
        profile = UserEpistemicModel().profile_user("minh")

        self.assertEqual(profile["knowledge_level"], "beginner")
        self.assertEqual(profile["tracking_scope"], "epistemic_understanding_only")
        self.assertIn("impermanence", profile["concept_familiarity"])

    def test_dharma_path_keeps_foundational_concepts_first(self):
        profile = UserEpistemicModel().profile_user("minh_vajrayana_advanced")
        path = DharmaPathEngine().generate_path(profile)

        self.assertEqual(path["ordered_concepts"][:5], [
            "impermanence",
            "suffering",
            "karma",
            "rebirth",
            "nirvana",
        ])
        self.assertIn("bardo", path["ordered_concepts"])
        self.assertTrue(path["prerequisites_respected"])

    def test_learning_state_tracker_recommends_confused_nodes_for_review(self):
        tracker = LearningStateTracker()

        state = tracker.update_state(
            "user-1",
            seen_nodes=["impermanence"],
            confused_nodes=["emptiness"],
        )

        self.assertEqual(state["recommended_review"], ["emptiness"])

    def test_adaptive_explainer_refuses_without_validated_context(self):
        profile = UserEpistemicModel().profile_user("minh")

        explanation = AdaptiveExplainer().explain("death", profile, [])

        self.assertEqual(explanation["confidence"], 0.0)
        self.assertIn("Insufficient verified data", explanation["explanation"])

    def test_adaptive_explainer_changes_tone_by_user_depth(self):
        profile = UserEpistemicModel().profile_user("minh_advanced")

        explanation = AdaptiveExplainer().explain(
            "impermanence",
            profile,
            self.validated_context(),
        )

        self.assertEqual(explanation["tone"], "epistemic-analytical")
        self.assertEqual(explanation["used_nodes"], ["impermanence"])

    def test_progression_mapper_never_claims_spiritual_attainment(self):
        profile = UserEpistemicModel().profile_user("minh")
        state = {
            "seen_nodes": ["impermanence"],
            "mastered_nodes": ["suffering"],
            "confused_nodes": [],
        }

        progress = ProgressionMapper().map_progress(profile, state)

        self.assertIn("realization", progress["states"])
        self.assertIn("conceptual integration only", progress["state_note"])


if __name__ == "__main__":
    unittest.main()
