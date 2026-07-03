from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_corpus_dashboard import (  # noqa: E402
    build_corpus_dashboard_file,
    build_dashboard,
    render_markdown_report,
)


def evidence_node(
    node_id: str,
    quality_score: int,
    review_status: str = "human_reviewed",
    curated_status: str = "curated",
    **overrides: str,
) -> dict:
    node = {
        "id": node_id,
        "type": "Evidence",
        "evidence_text": "Đây là một đoạn Evidence đủ dài để kiểm tra dashboard.",
        "start_time": "00:01:18.720",
        "end_time": "00:01:39.030",
        "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
        "citation_url": "https://www.youtube.com/watch?v=FISpARohzy8&t=78s",
        "document_id": "document_transcript_fisp_arohzy8",
        "speaker": "HT. Thích Giác Khang",
        "evidence_type": "transcript_excerpt",
        "confidence": "low",
        "review_status": review_status,
        "curated_status": curated_status,
        "quality_score": quality_score,
        "quality_flags": ["has_text", "has_citation_url"],
    }
    node.update(overrides)
    return node


def sample_payload() -> dict:
    return {
        "metadata": {"index_name": "giac_khang_curated_evidence_index"},
        "nodes": [
            evidence_node("evidence_0001", 95),
            evidence_node(
                "evidence_0002",
                65,
                citation_url="",
                speaker="",
                start_time="00:02:00.000",
                end_time="00:02:20.000",
            ),
            evidence_node(
                "evidence_0003",
                35,
                review_status="unreviewed",
                curated_status="",
                evidence_text="",
                start_time="",
                end_time="",
                citation_url="",
                evidence_type="",
                confidence="",
            ),
            {
                "id": "concept_kinh_sau_sau",
                "type": "Concept",
                "name": "Kinh Sáu Sáu",
            },
        ],
    }


def write_json(path: Path, payload: dict) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


class BuildCorpusDashboardTest(unittest.TestCase):
    def test_builds_markdown_report(self) -> None:
        dashboard = build_dashboard(
            sample_payload(),
            input_path=Path("curated_evidence_index.json"),
            generated_at="2026-07-03T14:00:00+07:00",
        )
        markdown = render_markdown_report(dashboard)

        self.assertIn("# Giác Khang Corpus Dashboard", markdown)
        self.assertIn("## Summary", markdown)
        self.assertIn("Total Evidence", markdown)

    def test_counts_total_evidence(self) -> None:
        dashboard = build_dashboard(sample_payload(), Path("index.json"))

        self.assertEqual(dashboard["metrics"]["total_evidence"], 3)

    def test_counts_human_reviewed_and_curated(self) -> None:
        dashboard = build_dashboard(sample_payload(), Path("index.json"))

        self.assertEqual(dashboard["metrics"]["human_reviewed_count"], 2)
        self.assertEqual(dashboard["metrics"]["curated_count"], 2)

    def test_counts_citation_url(self) -> None:
        dashboard = build_dashboard(sample_payload(), Path("index.json"))

        self.assertEqual(dashboard["citation_readiness"]["has_citation_url_count"], 1)
        self.assertEqual(
            dashboard["citation_readiness"]["missing_citation_url_count"], 2
        )

    def test_counts_quality_buckets(self) -> None:
        dashboard = build_dashboard(sample_payload(), Path("index.json"))

        self.assertEqual(dashboard["metrics"]["high_quality_count"], 1)
        self.assertEqual(dashboard["metrics"]["medium_quality_count"], 1)
        self.assertEqual(dashboard["metrics"]["needs_review_count"], 1)

    def test_detects_missing_metadata(self) -> None:
        dashboard = build_dashboard(sample_payload(), Path("index.json"))

        self.assertEqual(dashboard["metadata_gaps"]["missing_evidence_text_count"], 1)
        self.assertEqual(dashboard["metadata_gaps"]["missing_start_time_count"], 1)
        self.assertEqual(dashboard["metadata_gaps"]["missing_end_time_count"], 1)
        self.assertEqual(dashboard["metadata_gaps"]["missing_speaker_count"], 1)
        self.assertEqual(dashboard["metadata_gaps"]["missing_evidence_type_count"], 1)
        self.assertEqual(dashboard["metadata_gaps"]["missing_confidence_count"], 1)

    def test_includes_recommendations(self) -> None:
        dashboard = build_dashboard(sample_payload(), Path("index.json"))

        self.assertIn(
            "Continue batch ingestion", " ".join(dashboard["recommendations"])
        )
        self.assertIn("batch_review_helper", " ".join(dashboard["recommendations"]))

    def test_writes_valid_json_and_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            input_path = root / "curated_evidence_index.json"
            output_md = root / "corpus_dashboard.md"
            output_json = root / "corpus_dashboard.json"
            write_json(input_path, sample_payload())

            build_corpus_dashboard_file(input_path, output_md, output_json)
            written = json.loads(output_json.read_text(encoding="utf-8"))

            self.assertTrue(output_md.exists())
            self.assertEqual(
                written["metadata"]["dashboard_name"],
                "giac_khang_corpus_dashboard",
            )
            self.assertEqual(written["metrics"]["total_evidence"], 3)


if __name__ == "__main__":
    unittest.main()
