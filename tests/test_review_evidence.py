from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from review_evidence import build_review_queue, create_review_queue  # noqa: E402


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    seen: set[str] = set()
    output = {}

    for key, value in pairs:
        if key in seen:
            raise ValueError(f"Duplicate JSON key: {key}")
        seen.add(key)
        output[key] = value

    return output


def sample_payload() -> dict:
    return {
        "nodes": [
            {
                "id": "evidence_fisp_arohzy8_0001",
                "type": "Evidence",
                "name": "VTT caption excerpt 0001 from FISpARohzy8",
                "evidence_text": "Tiếp tục bài kinh 66",
                "evidence_type": "transcript_excerpt",
                "language": "vi",
                "confidence": "low",
                "source_kind": "youtube",
                "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
                "document_id": "document_transcript_fisp_arohzy8",
                "start_time": "00:01:18.720",
                "end_time": "00:01:39.030",
                "speaker": "HT. Thích Giác Khang",
                "review_status": "unreviewed",
                "notes": "Imported from YouTube VTT caption.",
            },
            {
                "id": "concept_sau_can",
                "type": "Concept",
                "name": "sáu căn",
            },
        ],
        "relationships": [
            {
                "source": "evidence_fisp_arohzy8_0001",
                "type": "HAS_CITATION",
                "target": "citation_youtube_fisp_arohzy8",
            }
        ],
    }


class ReviewEvidenceTest(unittest.TestCase):
    def test_creates_review_queue(self) -> None:
        queue = build_review_queue(sample_payload())

        self.assertEqual(len(queue["nodes"]), 1)
        self.assertEqual(queue["nodes"][0]["id"], "evidence_fisp_arohzy8_0001")

    def test_preserves_original_evidence_text(self) -> None:
        queue = build_review_queue(sample_payload())
        node = queue["nodes"][0]

        self.assertEqual(node["original_evidence_text"], "Tiếp tục bài kinh 66")
        self.assertEqual(node["evidence_text"], "Tiếp tục bài kinh 66")

    def test_initializes_reviewed_evidence_text(self) -> None:
        queue = build_review_queue(sample_payload())
        node = queue["nodes"][0]

        self.assertEqual(node["original_review_status"], "unreviewed")
        self.assertEqual(node["reviewed_evidence_text"], node["evidence_text"])
        self.assertEqual(node["reviewer"], "")
        self.assertEqual(node["reviewed_at"], "")
        self.assertEqual(node["review_notes"], "")
        self.assertEqual(node["review_status"], "unreviewed")

    def test_review_status_can_be_human_reviewed(self) -> None:
        queue = build_review_queue(sample_payload(), review_status="human_reviewed")
        node = queue["nodes"][0]

        self.assertEqual(node["original_review_status"], "unreviewed")
        self.assertEqual(node["review_status"], "human_reviewed")

    def test_does_not_mutate_source_evidence_file(self) -> None:
        payload = sample_payload()

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "source.json"
            output_path = Path(tmpdir) / "review_queue.json"
            input_path.write_text(
                json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            original_source_text = input_path.read_text(encoding="utf-8")

            create_review_queue(input_path, output_path)

            self.assertEqual(
                input_path.read_text(encoding="utf-8"), original_source_text
            )

    def test_preserves_timestamps(self) -> None:
        queue = build_review_queue(sample_payload())
        node = queue["nodes"][0]

        self.assertEqual(node["start_time"], "00:01:18.720")
        self.assertEqual(node["end_time"], "00:01:39.030")

    def test_preserves_source_url(self) -> None:
        queue = build_review_queue(sample_payload())
        node = queue["nodes"][0]

        self.assertEqual(
            node["source_url"],
            "https://www.youtube.com/watch?v=FISpARohzy8",
        )

    def test_only_includes_evidence_nodes(self) -> None:
        queue = build_review_queue(sample_payload())

        self.assertEqual(
            [node["type"] for node in queue["nodes"]],
            ["Evidence"],
        )

    def test_writes_review_queue_file(self) -> None:
        payload = sample_payload()

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "source.json"
            output_path = Path(tmpdir) / "review_queue.json"
            input_path.write_text(
                json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            create_review_queue(input_path, output_path)
            written = json.loads(output_path.read_text(encoding="utf-8"))

            self.assertEqual(len(written["nodes"]), 1)
            self.assertEqual(
                written["nodes"][0]["reviewed_evidence_text"],
                "Tiếp tục bài kinh 66",
            )

    def test_written_review_queue_has_no_duplicate_review_status_keys(self) -> None:
        payload = sample_payload()

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "source.json"
            output_path = Path(tmpdir) / "review_queue.json"
            input_path.write_text(
                json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            create_review_queue(
                input_path,
                output_path,
                review_status="human_reviewed",
            )

            raw_output = output_path.read_text(encoding="utf-8")
            parsed = json.loads(raw_output, object_pairs_hook=reject_duplicate_keys)

            self.assertEqual(parsed["nodes"][0]["original_review_status"], "unreviewed")
            self.assertEqual(parsed["nodes"][0]["review_status"], "human_reviewed")


if __name__ == "__main__":
    unittest.main()
