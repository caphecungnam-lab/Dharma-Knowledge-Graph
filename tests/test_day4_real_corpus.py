from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from dkg_api.app.ingestion.day4_extractor import Day4Extractor
from scripts.day4_drift_detection import detect_drift
from scripts.day4_real_corpus_ingestion import (
    DEFAULT_SOURCE,
    clean_vtt,
    run_ingestion,
)
from scripts.day4_stress_test import stress_test


class Day4RealCorpusTest(unittest.TestCase):
    def test_day4_extractor_only_extracts_explicit_concepts(self):
        extractor = Day4Extractor()
        chunk = {
            "chunk_id": "chunk_001",
            "position": 0,
            "text": "Karma is mentioned here. The next sentence is general.",
        }

        result = extractor.extract(chunk, {"source_id": "source_real"})

        self.assertEqual(len(result["concepts"]), 1)
        self.assertEqual(result["concepts"][0]["canonical_label"], "karma")
        self.assertEqual(result["concepts"][0]["extraction_rule"], "explicit_mention_only")

    def test_day4_extractor_does_not_infer_missing_teachings(self):
        result = Day4Extractor().extract(
            {
                "chunk_id": "chunk_001",
                "position": 0,
                "text": "This passage speaks about careful practice without naming doctrine.",
            },
            {"source_id": "source_real"},
        )

        self.assertEqual(result["concepts"], [])
        self.assertEqual(result["relations"], [])

    def test_clean_vtt_preserves_real_vietnamese_text(self):
        text = clean_vtt(DEFAULT_SOURCE.read_text(encoding="utf-8"))

        self.assertIn("Tiếp tục bài kinh 66", text)
        self.assertNotIn("WEBVTT", text)

    def test_real_corpus_ingestion_outputs_traceable_nodes(self):
        report = run_ingestion(
            [
                {
                    "path": str(DEFAULT_SOURCE),
                    "source_id": "source_youtube_fisp_arohzy8",
                    "title": "1A. KINH 6 6 L2CÂU 1 P1",
                    "tradition": "theravada",
                    "author": "HT. Thích Giác Khang",
                    "language": "vi",
                    "source_type": "dharma_talk",
                }
            ],
            chunk_limit=2,
        )

        self.assertEqual(report["status"], "ok")
        self.assertGreater(report["nodes_accepted"], 0)
        for document in report["documents"]:
            for node in document["accepted_nodes"]:
                self.assertTrue(node["traceability"]["sources"])
                self.assertTrue((node["match"] or {}).get("chunk_id"))

    def test_ingestion_failure_returns_structured_error(self):
        report = run_ingestion(
            [
                {
                    "path": "missing.txt",
                    "source_id": "missing_source",
                    "title": "Missing",
                    "tradition": "unknown",
                    "author": "unknown",
                    "language": "en",
                    "source_type": "text",
                }
            ]
        )

        self.assertEqual(report["status"], "rejected")
        self.assertEqual(report["documents"][0]["stage"], "corpus")
        self.assertEqual(report["documents"][0]["source_id"], "missing_source")

    def test_drift_detection_flags_inconsistent_concept(self):
        report = {
            "documents": [
                {
                    "accepted_nodes": [
                        {
                            "node_id": "concept_death",
                            "tradition": "theravada",
                            "epistemic_type": "doctrinal_view",
                            "confidence": 0.8,
                            "match": {"definition": "Death appears one way."},
                        },
                        {
                            "node_id": "concept_death",
                            "tradition": "vajrayana",
                            "epistemic_type": "esoteric_view",
                            "confidence": 0.8,
                            "match": {"definition": "Death appears another way."},
                        },
                    ]
                }
            ]
        }

        drift = detect_drift(report)

        self.assertTrue(drift["drift_detected"])
        self.assertEqual(drift["severity"], "medium")
        self.assertIn("concept_death", drift["affected_concepts"])

    def test_stress_test_does_not_crash_on_noisy_real_text(self):
        report = stress_test(6)

        self.assertFalse(report["stress"]["crashed"])
        self.assertIn(report["status"], {"ok", "rejected"})
        self.assertIn("rejection_reasons", report)


if __name__ == "__main__":
    unittest.main()
