from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from promote_reviewed_evidence import (  # noqa: E402
    promote_reviewed_evidence,
    promote_reviewed_evidence_file,
)


def evidence_node(
    node_id: str,
    review_status: str,
    reviewed_text: str = "Bản đã được người xem sửa.",
) -> dict:
    return {
        "id": node_id,
        "type": "Evidence",
        "name": f"Evidence {node_id}",
        "evidence_text": "Bản nhập thô.",
        "evidence_type": "transcript_excerpt",
        "language": "vi",
        "confidence": "low",
        "source_kind": "youtube",
        "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
        "document_id": "document_transcript_fisp_arohzy8",
        "start_time": "00:01:18.720",
        "end_time": "00:01:39.030",
        "speaker": "HT. Thích Giác Khang",
        "notes": "Imported from YouTube VTT caption.",
        "original_review_status": "unreviewed",
        "original_evidence_text": "Bản nhập thô.",
        "reviewed_evidence_text": reviewed_text,
        "reviewer": "Minh",
        "reviewed_at": "2026-07-03",
        "review_notes": "Checked transcript wording.",
        "review_status": review_status,
    }


def sample_payload() -> dict:
    return {
        "nodes": [
            evidence_node("evidence_fisp_arohzy8_0001", "human_reviewed"),
            evidence_node("evidence_fisp_arohzy8_0002", "unreviewed"),
            {
                "id": "concept_sau_can",
                "type": "Concept",
                "name": "Sáu căn",
            },
        ],
        "relationships": [
            {
                "source": "evidence_fisp_arohzy8_0001",
                "type": "HAS_CITATION",
                "target": "citation_youtube_fisp_arohzy8",
            },
            {
                "source": "evidence_fisp_arohzy8_0001",
                "type": "DERIVED_FROM",
                "target": "document_transcript_fisp_arohzy8",
            },
            {
                "source": "evidence_fisp_arohzy8_0002",
                "type": "HAS_CITATION",
                "target": "citation_youtube_fisp_arohzy8",
            },
            {
                "source": "evidence_fisp_arohzy8_0001",
                "type": "RELATED_TO",
                "target": "concept_missing_from_curated_output",
            },
        ],
    }


class PromoteReviewedEvidenceTest(unittest.TestCase):
    def test_promotes_only_human_reviewed_evidence(self) -> None:
        curated = promote_reviewed_evidence(sample_payload())

        self.assertEqual(
            [node["id"] for node in curated["nodes"]],
            ["evidence_fisp_arohzy8_0001"],
        )

    def test_skips_unreviewed_evidence(self) -> None:
        curated = promote_reviewed_evidence(sample_payload())
        node_ids = {node["id"] for node in curated["nodes"]}

        self.assertNotIn("evidence_fisp_arohzy8_0002", node_ids)

    def test_uses_reviewed_evidence_text_as_evidence_text(self) -> None:
        curated = promote_reviewed_evidence(sample_payload())
        node = curated["nodes"][0]

        self.assertEqual(node["evidence_text"], "Bản đã được người xem sửa.")
        self.assertEqual(node["reviewed_evidence_text"], "Bản đã được người xem sửa.")

    def test_preserves_original_evidence_text(self) -> None:
        curated = promote_reviewed_evidence(sample_payload())

        self.assertEqual(curated["nodes"][0]["original_evidence_text"], "Bản nhập thô.")

    def test_preserves_timestamps(self) -> None:
        curated = promote_reviewed_evidence(sample_payload())
        node = curated["nodes"][0]

        self.assertEqual(node["start_time"], "00:01:18.720")
        self.assertEqual(node["end_time"], "00:01:39.030")

    def test_preserves_source_url(self) -> None:
        curated = promote_reviewed_evidence(sample_payload())

        self.assertEqual(
            curated["nodes"][0]["source_url"],
            "https://www.youtube.com/watch?v=FISpARohzy8",
        )

    def test_preserves_core_evidence_fields(self) -> None:
        curated = promote_reviewed_evidence(sample_payload())
        node = curated["nodes"][0]

        self.assertEqual(node["document_id"], "document_transcript_fisp_arohzy8")
        self.assertEqual(node["speaker"], "HT. Thích Giác Khang")
        self.assertEqual(node["source_kind"], "youtube")
        self.assertEqual(node["language"], "vi")
        self.assertEqual(node["evidence_type"], "transcript_excerpt")
        self.assertEqual(node["confidence"], "low")

    def test_writes_curated_status(self) -> None:
        curated = promote_reviewed_evidence(sample_payload())
        node = curated["nodes"][0]

        self.assertEqual(node["curated_status"], "curated")
        self.assertEqual(node["curated_at"], "2026-07-03")
        self.assertEqual(node["curator"], "Minh")

    def test_does_not_mark_evidence_as_verified(self) -> None:
        curated = promote_reviewed_evidence(sample_payload())
        node = curated["nodes"][0]

        self.assertEqual(node["review_status"], "human_reviewed")
        self.assertNotEqual(node.get("review_status"), "verified")
        self.assertNotEqual(node.get("curated_status"), "verified")

    def test_preserves_relationships_for_promoted_evidence(self) -> None:
        curated = promote_reviewed_evidence(sample_payload())

        self.assertEqual(
            curated["relationships"],
            [
                {
                    "source": "evidence_fisp_arohzy8_0001",
                    "type": "DERIVED_FROM",
                    "target": "document_transcript_fisp_arohzy8",
                },
                {
                    "source": "evidence_fisp_arohzy8_0001",
                    "type": "HAS_CITATION",
                    "target": "citation_youtube_fisp_arohzy8",
                },
            ],
        )

    def test_skips_relationships_to_missing_non_source_nodes(self) -> None:
        curated = promote_reviewed_evidence(sample_payload())

        self.assertNotIn(
            {
                "source": "evidence_fisp_arohzy8_0001",
                "type": "RELATED_TO",
                "target": "concept_missing_from_curated_output",
            },
            curated["relationships"],
        )

    def test_writes_curated_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "review_queue.json"
            output_path = Path(tmpdir) / "evidence_curated.json"
            input_path.write_text(
                json.dumps(sample_payload(), indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            promote_reviewed_evidence_file(input_path, output_path)
            written = json.loads(output_path.read_text(encoding="utf-8"))

            self.assertEqual(len(written["nodes"]), 1)
            self.assertEqual(written["nodes"][0]["curated_status"], "curated")


if __name__ == "__main__":
    unittest.main()
