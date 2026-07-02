from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_graph import build_explorer_scopes, build_graph  # noqa: E402


class BuildGraphScopeTest(unittest.TestCase):
    def test_explorer_default_mode_is_giac_khang(self) -> None:
        scopes = build_explorer_scopes()

        self.assertEqual(scopes["default_mode"], "giac_khang")
        self.assertEqual(
            set(scopes["modes"]),
            {"giac_khang", "seeds_only", "all_data"},
        )

    def test_giac_khang_mode_excludes_old_demo_seed_files(self) -> None:
        graph = build_graph("giac_khang")
        source_files = set(graph["metadata"]["source_files"])

        self.assertIn(
            "data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json",
            source_files,
        )
        self.assertNotIn("data/seeds/giac_khang_pilot.json", source_files)
        self.assertNotIn("data/seeds/heart_sutra.json", source_files)
        self.assertNotIn("data/seeds/dhammapada.json", source_files)
        self.assertNotIn("data/seeds/concepts.json", source_files)
        self.assertNotIn("data/seeds/places_traditions.json", source_files)

    def test_giac_khang_mode_loads_processed_reviewed_and_curated_evidence(
        self,
    ) -> None:
        graph = build_graph("giac_khang")
        source_files = set(graph["metadata"]["source_files"])
        node_by_id = {node["id"]: node for node in graph["nodes"]}

        self.assertIn(
            "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
            source_files,
        )
        self.assertIn(
            "data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json",
            source_files,
        )
        self.assertIn(
            "data/curated/giac_khang/FISpARohzy8/evidence_curated.json",
            source_files,
        )
        self.assertEqual(
            node_by_id["evidence_fisp_arohzy8_0001"]["source_badge"],
            "curated",
        )
        self.assertEqual(
            node_by_id["corpus_giac_khang"]["source_badge"],
            "corpus",
        )
        self.assertEqual(
            node_by_id["source_youtube_fisp_arohzy8"]["source_badge"],
            "pilot",
        )
        self.assertEqual(
            node_by_id["citation_youtube_fisp_arohzy8"]["source_badge"],
            "pilot",
        )

    def test_seeds_only_mode_loads_only_seed_files(self) -> None:
        graph = build_graph("seeds_only")

        self.assertTrue(
            all(
                source_file.startswith("data/seeds/")
                for source_file in graph["metadata"]["source_files"]
            )
        )

    def test_all_data_mode_includes_seed_and_evidence_outputs(self) -> None:
        graph = build_graph("all_data")
        source_files = set(graph["metadata"]["source_files"])

        self.assertIn("data/seeds/heart_sutra.json", source_files)
        self.assertIn(
            "data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json",
            source_files,
        )
        self.assertIn(
            "data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json",
            source_files,
        )
        self.assertIn(
            "data/curated/giac_khang/FISpARohzy8/evidence_curated.json",
            source_files,
        )


if __name__ == "__main__":
    unittest.main()
