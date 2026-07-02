from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from import_manual_transcript import (  # noqa: E402
    CITATION_ID,
    DOCUMENT_ID,
    SOURCE_ID,
    ManualTranscriptError,
    convert_manual_transcript,
)


def transcript_data(segment: dict) -> dict:
    return {
        "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
        "video_id": "FISpARohzy8",
        "title": "1A. KINH 6 6 L2CÂU 1 P1",
        "speaker": "HT. Thích Giác Khang",
        "language": "vi",
        "segments": [segment],
    }


class ImportManualTranscriptTest(unittest.TestCase):
    def valid_segment(self) -> dict:
        return {
            "start_time": "00:00:00",
            "end_time": "00:00:30",
            "text": "Exact transcript text from the source.",
            "review_status": "unreviewed",
            "notes": "Test fixture text.",
        }

    def test_rejects_empty_text(self) -> None:
        segment = self.valid_segment()
        segment["text"] = ""

        with self.assertRaisesRegex(ManualTranscriptError, "empty text"):
            convert_manual_transcript(transcript_data(segment))

    def test_rejects_missing_start_time(self) -> None:
        segment = self.valid_segment()
        del segment["start_time"]

        with self.assertRaisesRegex(ManualTranscriptError, "missing start_time"):
            convert_manual_transcript(transcript_data(segment))

    def test_rejects_missing_end_time(self) -> None:
        segment = self.valid_segment()
        del segment["end_time"]

        with self.assertRaisesRegex(ManualTranscriptError, "missing end_time"):
            convert_manual_transcript(transcript_data(segment))

    def test_creates_evidence_node_with_correct_fields(self) -> None:
        converted = convert_manual_transcript(transcript_data(self.valid_segment()))

        self.assertEqual(len(converted["nodes"]), 1)
        node = converted["nodes"][0]
        self.assertEqual(node["id"], "evidence_fisp_arohzy8_0001")
        self.assertEqual(node["type"], "Evidence")
        self.assertEqual(node["evidence_type"], "transcript_excerpt")
        self.assertEqual(node["confidence"], "low")
        self.assertEqual(node["source_kind"], "youtube")
        self.assertEqual(
            node["source_url"],
            "https://www.youtube.com/watch?v=FISpARohzy8",
        )
        self.assertEqual(node["document_id"], DOCUMENT_ID)
        self.assertEqual(node["locator"], "00:00:00-00:00:30")
        self.assertEqual(node["speaker"], "HT. Thích Giác Khang")
        self.assertEqual(node["review_status"], "unreviewed")

        relationships = converted["relationships"]
        self.assertIn(
            {"source": DOCUMENT_ID, "type": "HAS_EVIDENCE", "target": node["id"]},
            relationships,
        )
        self.assertIn(
            {"source": node["id"], "type": "DERIVED_FROM", "target": DOCUMENT_ID},
            relationships,
        )
        self.assertIn(
            {"source": node["id"], "type": "DERIVED_FROM", "target": SOURCE_ID},
            relationships,
        )
        self.assertIn(
            {"source": node["id"], "type": "HAS_CITATION", "target": CITATION_ID},
            relationships,
        )


if __name__ == "__main__":
    unittest.main()
