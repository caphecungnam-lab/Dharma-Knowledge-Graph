from __future__ import annotations

import unittest

from dkg_api.app.services.epistemic_ui_adapter import EpistemicUIAdapter
from dkg_api.app.services.graph_visualization_engine import GraphVisualizationEngine
from dkg_api.app.services.pathfinding_engine import PathfindingEngine
from dkg_api.app.services.tradition_overlay_engine import TraditionOverlayEngine


class Phase4KnowledgeExperienceTest(unittest.TestCase):
    def graph_data(self):
        return {
            "nodes": [
                {
                    "id": "death",
                    "label": "death",
                    "tradition": "shared_core",
                    "epistemic_type": "doctrinal_view",
                    "confidence": 0.9,
                },
                {
                    "id": "bardo",
                    "label": "bardo",
                    "tradition": "vajrayana",
                    "epistemic_type": "esoteric_view",
                    "confidence": 0.65,
                },
            ],
            "edges": [
                {
                    "from": "death",
                    "to": "bardo",
                    "type": "DOCTRINAL_CONFLICT",
                    "strength": 0.7,
                }
            ],
        }

    def test_visualization_engine_builds_required_map_shape(self):
        engine = GraphVisualizationEngine()

        result = engine.build_map("death", self.graph_data())

        self.assertEqual(result["map_id"], "map_death")
        self.assertEqual(result["center_node"], "death")
        self.assertIn("nodes", result)
        self.assertIn("edges", result)
        self.assertIn("clusters", result)
        self.assertIn("theravada", result["layers"])

    def test_ui_adapter_makes_low_confidence_nodes_faded(self):
        adapter = EpistemicUIAdapter()

        node = adapter.node({"id": "x", "label": "X", "confidence": 0.2}, 0, 1)

        self.assertEqual(node["visual_state"], "faded")

    def test_conflict_edge_gets_visual_label(self):
        adapter = EpistemicUIAdapter()

        edge = adapter.edge(
            {
                "from": "death",
                "to": "bardo",
                "type": "DOCTRINAL_CONFLICT",
                "strength": 0.7,
            }
        )

        self.assertEqual(edge["visual_label"], "doctrinal divergence")

    def test_tradition_overlay_keeps_layers_separate(self):
        engine = TraditionOverlayEngine()
        nodes = [
            {"id": "emptiness", "tradition": "mahayana"},
            {"id": "bardo", "tradition": "vajrayana"},
        ]

        overlay = engine.build_overlay("emptiness", nodes, [])

        self.assertEqual(overlay["mahayana"]["nodes"][0]["id"], "emptiness")
        self.assertEqual(overlay["vajrayana"]["nodes"][0]["id"], "bardo")

    def test_pathfinding_engine_adds_epistemic_step_metadata(self):
        engine = PathfindingEngine()

        path = engine.build_path(
            [
                {
                    "from": "death",
                    "to": "impermanence",
                    "type": "RELATED_TO",
                    "confidence": 0.8,
                    "tradition": "theravada",
                }
            ]
        )

        self.assertEqual(path[0]["epistemic_confidence"], 0.8)
        self.assertEqual(path[0]["tradition_relevance"], "theravada")


if __name__ == "__main__":
    unittest.main()
