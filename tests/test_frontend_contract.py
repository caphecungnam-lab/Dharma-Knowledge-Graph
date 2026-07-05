from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"


class FrontendContractTest(unittest.TestCase):
    def test_frontend_uses_required_stack(self):
        package = json.loads((FRONTEND / "package.json").read_text())
        dependencies = package["dependencies"]

        self.assertIn("next", dependencies)
        self.assertIn("cytoscape", dependencies)
        self.assertIn("zustand", dependencies)
        self.assertIn("tailwindcss", package["devDependencies"])
        self.assertIn("typescript", package["devDependencies"])

    def test_five_zone_components_exist(self):
        expected = [
            "QueryPortal.tsx",
            "KnowledgeGraphCanvas.tsx",
            "ConceptInspector.tsx",
            "TraditionOverlayPanel.tsx",
            "LearningPathView.tsx",
        ]

        for filename in expected:
            self.assertTrue((FRONTEND / "components" / filename).exists())

    def test_ui_is_not_chat_oriented(self):
        page = (FRONTEND / "app/page.tsx").read_text()
        portal = (FRONTEND / "components/QueryPortal.tsx").read_text()

        self.assertNotIn("chat", page.lower())
        self.assertNotIn("chat", portal.lower())
        self.assertIn("Enter knowledge space", portal)

    def test_zustand_store_tracks_required_state(self):
        store = (FRONTEND / "store/useKnowledgeStore.ts").read_text()

        for key in (
            "currentGraph",
            "selectedNode",
            "activeTraditions",
            "userPath",
            "queryHistory",
        ):
            self.assertIn(key, store)

    def test_graph_canvas_uses_epistemic_visual_mapping(self):
        canvas = (FRONTEND / "components/KnowledgeGraphCanvas.tsx").read_text()

        self.assertIn("colorByType", canvas)
        self.assertIn("core_fact", canvas)
        self.assertIn("esoteric", canvas)
        self.assertIn("cytoscape", canvas)


if __name__ == "__main__":
    unittest.main()
