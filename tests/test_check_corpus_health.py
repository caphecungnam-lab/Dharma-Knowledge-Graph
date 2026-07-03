from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_corpus_health import check_corpus_health, main  # noqa: E402


def evidence_node(node_id: str = "evidence_0001", **overrides: object) -> dict:
    node = {
        "id": node_id,
        "type": "Evidence",
        "evidence_text": "Đây là một Evidence node đủ tốt cho health gate.",
        "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
        "start_time": "00:01:18.720",
        "end_time": "00:01:39.030",
        "citation_url": "https://www.youtube.com/watch?v=FISpARohzy8&t=78s",
        "speaker": "HT. Thích Giác Khang",
        "evidence_type": "transcript_excerpt",
        "confidence": "low",
        "review_status": "human_reviewed",
        "curated_status": "curated",
        "quality_score": 95,
    }
    node.update(overrides)
    return node


def payload(nodes: list[dict]) -> dict:
    return {"nodes": nodes, "relationships": []}


def write_json(path: Path, data: dict) -> None:
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


class CheckCorpusHealthTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.path = Path(self.temp_dir.name) / "curated_evidence_index.json"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_payload(self, nodes: list[dict]) -> None:
        write_json(self.path, payload(nodes))

    def test_passes_healthy_corpus(self) -> None:
        self.write_payload([evidence_node()])

        result = check_corpus_health(self.path)

        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["evidence_count"], 1)
        self.assertEqual(result["errors"], [])

    def test_fails_when_no_evidence(self) -> None:
        self.write_payload([])

        result = check_corpus_health(self.path)

        self.assertEqual(result["status"], "fail")
        self.assertIn("No Evidence nodes found.", result["errors"])

    def test_fails_duplicate_evidence_ids(self) -> None:
        self.write_payload([evidence_node(), evidence_node()])

        result = check_corpus_health(self.path)

        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["metrics"]["duplicate_ids"], 1)

    def test_fails_missing_evidence_text(self) -> None:
        self.write_payload([evidence_node(evidence_text="")])

        result = check_corpus_health(self.path)

        self.assertEqual(result["status"], "fail")
        self.assertIn("missing evidence_text", " ".join(result["errors"]))

    def test_fails_missing_source_url(self) -> None:
        self.write_payload([evidence_node(source_url="")])

        result = check_corpus_health(self.path)

        self.assertEqual(result["status"], "fail")
        self.assertIn("missing source_url", " ".join(result["errors"]))

    def test_fails_missing_start_time(self) -> None:
        self.write_payload([evidence_node(start_time="")])

        result = check_corpus_health(self.path)

        self.assertEqual(result["status"], "fail")
        self.assertIn("missing start_time", " ".join(result["errors"]))

    def test_fails_missing_end_time(self) -> None:
        self.write_payload([evidence_node(end_time="")])

        result = check_corpus_health(self.path)

        self.assertEqual(result["status"], "fail")
        self.assertIn("missing end_time", " ".join(result["errors"]))

    def test_fails_low_quality_evidence(self) -> None:
        self.write_payload([evidence_node(quality_score=40)])

        result = check_corpus_health(self.path)

        self.assertEqual(result["status"], "fail")
        self.assertIn("below min 50", " ".join(result["errors"]))

    def test_warns_missing_citation_url(self) -> None:
        self.write_payload([evidence_node(citation_url="")])

        result = check_corpus_health(self.path)

        self.assertEqual(result["status"], "pass")
        self.assertIn("missing citation_url", " ".join(result["warnings"]))

    def test_strict_mode_fails_on_warnings(self) -> None:
        self.write_payload([evidence_node(citation_url="")])

        result = check_corpus_health(self.path, strict=True)

        self.assertEqual(result["status"], "fail")

    def test_json_output_is_valid(self) -> None:
        self.write_payload([evidence_node()])
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            exit_code = main(["--input", str(self.path), "--json"])

        parsed = json.loads(stdout.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(parsed["status"], "pass")

    def test_exit_code_behavior_is_correct(self) -> None:
        self.write_payload([evidence_node(quality_score=40)])
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            exit_code = main(["--input", str(self.path)])

        self.assertEqual(exit_code, 1)
        self.assertIn("Status: FAIL", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
