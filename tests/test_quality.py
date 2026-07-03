from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dharma_kg.quality import get_quality_flags, score_evidence  # noqa: E402


def evidence_node(**overrides: str) -> dict:
    node = {
        "id": "evidence_test_0001",
        "type": "Evidence",
        "evidence_text": "This Evidence text is long enough to score.",
        "start_time": "00:02:37.959",
        "end_time": "00:02:54.470",
        "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
        "speaker": "HT. Thích Giác Khang",
        "evidence_type": "transcript_excerpt",
        "confidence": "low",
        "review_status": "unreviewed",
        "curated_status": "",
    }
    node.update(overrides)
    return node


class QualityTest(unittest.TestCase):
    def test_scores_text_evidence_correctly(self) -> None:
        quality = score_evidence(evidence_node())

        self.assertEqual(quality["quality_score"], 75)

    def test_missing_text_gets_lower_score(self) -> None:
        with_text = score_evidence(evidence_node())["quality_score"]
        without_text = score_evidence(evidence_node(evidence_text=""))["quality_score"]

        self.assertLess(without_text, with_text)

    def test_human_reviewed_adds_score(self) -> None:
        unreviewed = score_evidence(evidence_node())["quality_score"]
        reviewed = score_evidence(evidence_node(review_status="human_reviewed"))[
            "quality_score"
        ]

        self.assertEqual(reviewed - unreviewed, 15)

    def test_verified_adds_score(self) -> None:
        unreviewed = score_evidence(evidence_node())["quality_score"]
        verified = score_evidence(evidence_node(review_status="verified"))[
            "quality_score"
        ]

        self.assertEqual(verified - unreviewed, 20)

    def test_curated_adds_score(self) -> None:
        uncurated = score_evidence(evidence_node())["quality_score"]
        curated = score_evidence(evidence_node(curated_status="curated"))[
            "quality_score"
        ]

        self.assertEqual(curated - uncurated, 10)

    def test_citation_url_adds_score(self) -> None:
        without_citation = score_evidence(
            evidence_node(source_url="https://example.com/source")
        )["quality_score"]
        with_citation = score_evidence(
            evidence_node(citation_url="https://example.com/citation")
        )["quality_score"]

        self.assertEqual(with_citation - without_citation, 10)

    def test_score_capped_at_100(self) -> None:
        quality = score_evidence(
            evidence_node(
                review_status="verified",
                curated_status="curated",
                citation_url="https://example.com/citation",
            )
        )

        self.assertEqual(quality["quality_score"], 100)

    def test_flags_are_generated_correctly(self) -> None:
        flags = get_quality_flags(
            evidence_node(review_status="human_reviewed", curated_status="curated")
        )

        self.assertIn("has_text", flags)
        self.assertIn("has_start_time", flags)
        self.assertIn("has_end_time", flags)
        self.assertIn("has_source_url", flags)
        self.assertIn("has_citation_url", flags)
        self.assertIn("human_reviewed", flags)
        self.assertIn("curated", flags)
        self.assertIn("has_speaker", flags)
        self.assertIn("has_evidence_type", flags)
        self.assertIn("has_confidence", flags)


if __name__ == "__main__":
    unittest.main()
