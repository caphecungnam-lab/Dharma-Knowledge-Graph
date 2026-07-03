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
    DEFAULT_INPUT_PATH,
    build_debug_info,
    format_text_results,
    normalize_query_terms,
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
                "Bài giảng về kinh 66 và các pháp.",
                name="VTT caption excerpt about Kinh Sáu Sáu",
            ),
            evidence_node(
                "evidence_fisp_arohzy8_0002",
                "Nội dung nói về lục căn.",
                review_notes="Cần kiểm tra thuật ngữ Kinh Sáu Sáu.",
            ),
            evidence_node(
                "evidence_fisp_arohzy8_0003",
                "Nội dung nói về sáu trần và lục thức.",
            ),
            {
                "id": "concept_kinh_sau_sau",
                "type": "Concept",
                "name": "Kinh Sáu Sáu",
            },
        ]
    }


class SearchCuratedEvidenceTest(unittest.TestCase):
    def test_default_path_uses_curated_index(self) -> None:
        self.assertEqual(
            DEFAULT_INPUT_PATH,
            Path("data") / "indexes" / "giac_khang" / "curated_evidence_index.json",
        )

    def test_case_insensitive_search_preserves_vietnamese_unicode(self) -> None:
        results = search_curated_evidence(sample_payload(), "kinh sáu sáu")

        self.assertEqual(results[0]["id"], "evidence_fisp_arohzy8_0001")
        self.assertIn("kinh 66", results[0]["evidence_text"])

    def test_kinh_sau_sau_alias_finds_kinh_66(self) -> None:
        results = search_curated_evidence(sample_payload(), "Kinh Sáu Sáu")

        self.assertEqual(results[0]["id"], "evidence_fisp_arohzy8_0001")

    def test_sau_sau_alias_finds_66(self) -> None:
        results = search_curated_evidence(sample_payload(), "sáu sáu")

        self.assertEqual(results[0]["id"], "evidence_fisp_arohzy8_0001")

    def test_unaccented_query_matches_accented_text(self) -> None:
        results = search_curated_evidence(sample_payload(), "luc can")

        self.assertEqual(results[0]["id"], "evidence_fisp_arohzy8_0002")

    def test_luc_tran_and_luc_thuc_aliases_match_vietnamese_text(self) -> None:
        tran_results = search_curated_evidence(sample_payload(), "luc tran")
        thuc_results = search_curated_evidence(sample_payload(), "luc thuc")

        self.assertEqual(tran_results[0]["id"], "evidence_fisp_arohzy8_0003")
        self.assertEqual(thuc_results[0]["id"], "evidence_fisp_arohzy8_0003")

    def test_searches_review_notes(self) -> None:
        results = search_curated_evidence(sample_payload(), "thuật ngữ")

        self.assertEqual(
            [result["id"] for result in results], ["evidence_fisp_arohzy8_0002"]
        )

    def test_skips_non_evidence_nodes(self) -> None:
        results = search_curated_evidence(sample_payload(), "concept")

        self.assertEqual(results, [])

    def test_searches_name_field(self) -> None:
        results = search_curated_evidence(sample_payload(), "caption excerpt")

        self.assertEqual(results[0]["id"], "evidence_fisp_arohzy8_0001")

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
        self.assertEqual(result["video_id"], "FISpARohzy8")
        self.assertEqual(
            result["citation_url"],
            "https://www.youtube.com/watch?v=FISpARohzy8&t=78s",
        )
        self.assertEqual(result["quality_score"], 90)
        self.assertIn("has_text", result["quality_flags"])
        self.assertIn("HT. Thích Giác Khang", result["citation"])
        self.assertIn("00:01:18.720 -> 00:01:39.030", result["citation"])

    def test_format_text_results(self) -> None:
        results = search_curated_evidence(sample_payload(), "các pháp")
        output = format_text_results(results)

        self.assertIn("id: evidence_fisp_arohzy8_0001", output)
        self.assertIn("citation:", output)
        self.assertIn("source_url:", output)
        self.assertIn("Citation URL:", output)
        self.assertIn("https://www.youtube.com/watch?v=FISpARohzy8&t=78s", output)
        self.assertIn("Quality: 90 / 100", output)
        self.assertIn("Flags:", output)

    def test_search_curated_evidence_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "curated_evidence_index.json"
            path.write_text(
                json.dumps(sample_payload(), indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            results = search_curated_evidence_file("luc can", path=path)

            self.assertEqual(results[0]["id"], "evidence_fisp_arohzy8_0002")

    def test_search_finds_evidence_from_batch_curated_index(self) -> None:
        payload = {
            "metadata": {"index_name": "giac_khang_curated_evidence_index"},
            "nodes": [
                evidence_node(
                    "evidence_fisp_arohzy8_0007",
                    "Nội dung đã sửa ở đây.",
                    source_file=(
                        "data/curated/giac_khang/FISpARohzy8/"
                        "evidence_batch_001_curated.json"
                    ),
                )
            ],
            "relationships": [],
        }

        results = search_curated_evidence(payload, "Nội dung đã sửa")

        self.assertEqual(results[0]["id"], "evidence_fisp_arohzy8_0007")

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
            self.assertEqual(
                parsed[0]["citation_url"],
                "https://www.youtube.com/watch?v=FISpARohzy8&t=78s",
            )
            self.assertEqual(parsed[0]["quality_score"], 90)
            self.assertIn("has_text", parsed[0]["quality_flags"])

    def test_higher_quality_evidence_ranks_first_when_match_is_equal(self) -> None:
        payload = {
            "nodes": [
                evidence_node(
                    "evidence_low_quality",
                    "Matching phrase about Kinh Sáu Sáu.",
                    review_status="unreviewed",
                    curated_status="",
                    quality_score=40,
                    quality_flags=["has_text"],
                ),
                evidence_node(
                    "evidence_high_quality",
                    "Matching phrase about Kinh Sáu Sáu.",
                    review_status="human_reviewed",
                    curated_status="curated",
                    quality_score=95,
                    quality_flags=["has_text", "human_reviewed", "curated"],
                ),
            ]
        }

        results = search_curated_evidence(payload, "Matching phrase")

        self.assertEqual(results[0]["id"], "evidence_high_quality")

    def test_debug_info_does_not_crash(self) -> None:
        debug_info = build_debug_info(
            Path("data/curated/giac_khang/FISpARohzy8/evidence_curated.json"),
            sample_payload(),
            "Kinh Sáu Sáu",
        )

        self.assertEqual(debug_info["evidence_node_count"], 3)
        self.assertIn("kinh 66", debug_info["normalized_query_terms"])
        self.assertIn("name", debug_info["fields_searched"])

    def test_cli_debug_output(self) -> None:
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
                    "--debug",
                    "--limit",
                    "1",
                    "--path",
                    str(path),
                ],
                check=True,
                capture_output=True,
                encoding="utf-8",
            )

            self.assertIn("curated_file_path:", completed.stdout)
            self.assertIn("evidence_node_count: 3", completed.stdout)
            self.assertIn("normalized_query_terms:", completed.stdout)
            self.assertIn("fields_searched:", completed.stdout)
            self.assertIn("id: evidence_fisp_arohzy8_0001", completed.stdout)

    def test_normalize_query_terms(self) -> None:
        terms = normalize_query_terms("  Kinh   Sáu Sáu ")

        self.assertIn("kinh sau sau", terms)
        self.assertIn("bài kinh 66", terms)
        self.assertIn("bai kinh 66", terms)


if __name__ == "__main__":
    unittest.main()
