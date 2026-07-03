from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ask_curated_evidence import (  # noqa: E402
    DEFAULT_INPUT_PATH,
    NO_EVIDENCE_MESSAGE,
    answer_question,
    format_text_answer,
    question_search_queries,
)


def evidence_node(node_id: str, text: str, start_time: str = "00:01:18.720") -> dict:
    return {
        "id": node_id,
        "type": "Evidence",
        "evidence_text": text,
        "reviewed_evidence_text": text,
        "original_evidence_text": text,
        "name": f"Evidence {node_id}",
        "start_time": start_time,
        "end_time": "00:01:39.030",
        "speaker": "HT. Thích Giác Khang",
        "review_status": "human_reviewed",
        "curated_status": "curated",
        "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
        "quality_score": 90,
        "quality_flags": ["has_text", "human_reviewed", "curated"],
    }


def sample_payload() -> dict:
    return {
        "nodes": [
            evidence_node(
                "evidence_fisp_arohzy8_0001",
                "Tức là phần thứ nhất là trình bày về bài kinh 66 tức là 36 pháp toàn thể vũ trụ.",
            ),
            evidence_node(
                "evidence_fisp_arohzy8_0002",
                "Bài kinh 66 gồm tất cả là sáu phần.",
                start_time="00:01:39.040",
            ),
        ]
    }


class AskCuratedEvidenceTest(unittest.TestCase):
    def test_default_path_uses_curated_index(self) -> None:
        self.assertEqual(
            DEFAULT_INPUT_PATH,
            Path("data") / "indexes" / "giac_khang" / "curated_evidence_index.json",
        )

    def write_sample_file(self, tmpdir: str) -> Path:
        path = Path(tmpdir) / "curated_evidence_index.json"
        path.write_text(
            json.dumps(sample_payload(), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return path

    def test_question_search_queries_extracts_numeric_phrase(self) -> None:
        queries = question_search_queries("Sư Giác Khang nói gì về 36 pháp?")

        self.assertIn("36 pháp", queries)

    def test_answers_using_matched_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            answer = answer_question(
                "Sư Giác Khang nói gì về 36 pháp?",
                path=self.write_sample_file(tmpdir),
            )

            self.assertIn("36 pháp toàn thể vũ trụ", answer["answer"])
            self.assertEqual(
                answer["evidence"][0]["evidence_id"], "evidence_fisp_arohzy8_0001"
            )

    def test_answers_from_merged_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self.write_sample_file(tmpdir)
            answer = answer_question("Kinh Sáu Sáu", path=path)

            self.assertIn("bài kinh 66", answer["answer"].casefold())
            self.assertEqual(answer["evidence"][0]["video_id"], "FISpARohzy8")

    def test_includes_citation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            answer = answer_question(
                "Sư Giác Khang nói gì về 36 pháp?",
                path=self.write_sample_file(tmpdir),
            )

            self.assertIn("HT. Thích Giác Khang", answer["evidence"][0]["citation"])
            self.assertIn(
                "00:01:18.720 -> 00:01:39.030", answer["evidence"][0]["citation"]
            )
            self.assertEqual(
                answer["evidence"][0]["citation_url"],
                "https://www.youtube.com/watch?v=FISpARohzy8&t=78s",
            )

    def test_includes_source_url(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            answer = answer_question(
                "Sư Giác Khang nói gì về 36 pháp?",
                path=self.write_sample_file(tmpdir),
            )

            self.assertEqual(
                answer["evidence"][0]["source_url"],
                "https://www.youtube.com/watch?v=FISpARohzy8",
            )

    def test_includes_review_and_curated_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            answer = answer_question(
                "Sư Giác Khang nói gì về 36 pháp?",
                path=self.write_sample_file(tmpdir),
            )

            self.assertEqual(answer["evidence"][0]["review_status"], "human_reviewed")
            self.assertEqual(answer["evidence"][0]["curated_status"], "curated")
            self.assertEqual(answer["evidence"][0]["quality_score"], 90)

    def test_returns_no_evidence_message_when_no_match(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            answer = answer_question(
                "Không có chủ đề này",
                path=self.write_sample_file(tmpdir),
            )

            self.assertEqual(answer["answer"], NO_EVIDENCE_MESSAGE)
            self.assertEqual(answer["evidence"], [])

    def test_format_text_answer(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            answer = answer_question(
                "Sư Giác Khang nói gì về 36 pháp?",
                path=self.write_sample_file(tmpdir),
            )
            output = format_text_answer(answer)

            self.assertIn("question:", output)
            self.assertIn("answer:", output)
            self.assertIn("evidence id:", output)
            self.assertIn("citation:", output)
            self.assertIn("citation_url:", output)
            self.assertIn("quality_score:", output)

    def test_supports_json_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self.write_sample_file(tmpdir)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "ask_curated_evidence.py"),
                    "Sư Giác Khang nói gì về 36 pháp?",
                    "--json",
                    "--path",
                    str(path),
                ],
                check=True,
                capture_output=True,
                encoding="utf-8",
            )
            parsed = json.loads(completed.stdout)

            self.assertIn("36 pháp toàn thể vũ trụ", parsed["answer"])
            self.assertEqual(
                parsed["evidence"][0]["evidence_id"], "evidence_fisp_arohzy8_0001"
            )
            self.assertEqual(
                parsed["evidence"][0]["citation_url"],
                "https://www.youtube.com/watch?v=FISpARohzy8&t=78s",
            )
            self.assertEqual(parsed["evidence"][0]["quality_score"], 90)

    def test_respects_limit(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            answer = answer_question(
                "bài kinh 66",
                path=self.write_sample_file(tmpdir),
                limit=1,
            )

            self.assertEqual(len(answer["evidence"]), 1)

    def test_higher_quality_evidence_ranks_first_when_match_is_equal(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "curated_evidence_index.json"
            payload = {
                "nodes": [
                    evidence_node(
                        "evidence_low_quality",
                        "Matching phrase about Kinh Sáu Sáu.",
                    ),
                    evidence_node(
                        "evidence_high_quality",
                        "Matching phrase about Kinh Sáu Sáu.",
                    ),
                ]
            }
            payload["nodes"][0]["quality_score"] = 35
            payload["nodes"][1]["quality_score"] = 95
            path.write_text(
                json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            answer = answer_question("Matching phrase", path=path, limit=2)

            self.assertEqual(
                answer["evidence"][0]["evidence_id"],
                "evidence_high_quality",
            )


if __name__ == "__main__":
    unittest.main()
