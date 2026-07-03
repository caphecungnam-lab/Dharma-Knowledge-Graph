from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from search_curated_evidence import (  # noqa: E402
    format_text_results,
    search_curated_evidence,
    search_curated_evidence_file,
)


def evidence_node(node_id: str, evidence_text: str, **overrides: str) -> dict:
    node = {
        "id": node_id,
        "type": "Evidence",
        "evidence_text": evidence_text,
        "reviewed_evidence_text": evidence_text,
        "original_evidence_text": evidence_text,
        "notes": "Imported from YouTube VTT caption.",
        "review_notes": "",
        "start_time": "00:01:18.720",
        "end_time": "00:01:39.030",
        "speaker": "HT. Thích Giác Khang",
        "review_status": "human_reviewed",
        "curated_status": "curated",
        "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
    }
    node.update(overrides)
    return node


def sample_payload() -> dict:
    return {
        "nodes": [
            evidence_node(
                "evidence_fisp_arohzy8_0001",
                "Bài giảng về Kinh Sáu Sáu và các pháp.",
            ),
            evidence_node(
                "evidence_fisp_arohzy8_0002",
                "Nội dung nói về sáu căn.",
                review_notes="Cần kiểm tra thuật ngữ Kinh Sáu Sáu.",
            ),
            {
                "id": "concept_kinh_sau_sau",
                "type": "Concept",
                "name": "Kinh Sáu Sáu",
            },
        ]
    }


class SearchCuratedEvidenceTest(unittest.TestCase):
    def test_case_insensitive_search_preserves_vietnamese_unicode(self) -> None:
        results = search_curated_evidence(sample_payload(), "kinh sáu sáu")

        self.assertEqual(results[0]["id"], "evidence_fisp_arohzy8_0001")
        self.assertIn("Kinh Sáu Sáu", results[0]["evidence_text"])

    def test_searches_review_notes(self) -> None:
        results = search_curated_evidence(sample_payload(), "thuật ngữ")

        self.assertEqual(
            [result["id"] for result in results], ["evidence_fisp_arohzy8_0002"]
        )

    def test_skips_non_evidence_nodes(self) -> None:
        results = search_curated_evidence(sample_payload(), "concept")

        self.assertEqual(results, [])

    def test_limit_results(self) -> None:
        results = search_curated_evidence(sample_payload(), "Kinh Sáu Sáu", limit=1)

        self.assertEqual(len(results), 1)

    def test_result_contains_citation_fields(self) -> None:
        result = search_curated_evidence(sample_payload(), "các pháp")[0]

        self.assertEqual(result["start_time"], "00:01:18.720")
        self.assertEqual(result["end_time"], "00:01:39.030")
        self.assertEqual(result["speaker"], "HT. Thích Giác Khang")
        self.assertEqual(result["review_status"], "human_reviewed")
        self.assertEqual(result["curated_status"], "curated")
        self.assertEqual(
            result["source_url"],
            "https://www.youtube.com/watch?v=FISpARohzy8",
        )
        self.assertIn("HT. Thích Giác Khang", result["citation"])
        self.assertIn("00:01:18.720 -> 00:01:39.030", result["citation"])

    def test_format_text_results(self) -> None:
        results = search_curated_evidence(sample_payload(), "các pháp")
        output = format_text_results(results)

        self.assertIn("id: evidence_fisp_arohzy8_0001", output)
        self.assertIn("citation:", output)
        self.assertIn("source_url:", output)

    def test_search_curated_evidence_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "evidence_curated.json"
            path.write_text(
                json.dumps(sample_payload(), indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            results = search_curated_evidence_file("sáu căn", path=path)

            self.assertEqual(results[0]["id"], "evidence_fisp_arohzy8_0002")

    def test_cli_json_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "evidence_curated.json"
            path.write_text(
                json.dumps(sample_payload(), indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "search_curated_evidence.py"),
                    "Kinh Sáu Sáu",
                    "--json",
                    "--limit",
                    "1",
                    "--path",
                    str(path),
                ],
                check=True,
                capture_output=True,
                encoding="utf-8",
            )
            parsed = json.loads(completed.stdout)

            self.assertEqual(len(parsed), 1)
            self.assertEqual(parsed[0]["id"], "evidence_fisp_arohzy8_0001")


if __name__ == "__main__":
    unittest.main()
