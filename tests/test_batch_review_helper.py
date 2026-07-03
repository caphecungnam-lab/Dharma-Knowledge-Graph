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

from batch_review_helper import (  # noqa: E402
    approve_evidence,
    edit_evidence,
    init_review_queue,
    list_review_queue,
    main,
    reject_evidence,
    review_stats,
    show_evidence,
)
from promote_reviewed_evidence import (  # noqa: E402
    main as promote_main,
    promote_reviewed_evidence_file,
)


def evidence_node(
    node_id: str,
    text: str = "Bản nhập thô từ VTT.",
    review_status: str = "unreviewed",
) -> dict:
    return {
        "id": node_id,
        "type": "Evidence",
        "name": f"Evidence {node_id}",
        "evidence_text": text,
        "evidence_type": "transcript_excerpt",
        "language": "vi",
        "confidence": "low",
        "source_kind": "youtube",
        "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
        "document_id": "document_transcript_fisp_arohzy8",
        "start_time": "00:01:18.720",
        "end_time": "00:01:39.030",
        "speaker": "HT. Thích Giác Khang",
        "review_status": review_status,
        "notes": "Imported from YouTube VTT caption.",
    }


def sample_payload() -> dict:
    return {
        "nodes": [
            evidence_node("evidence_fisp_arohzy8_0001", "Đoạn một."),
            evidence_node("evidence_fisp_arohzy8_0002", "Đoạn hai."),
            {
                "id": "citation_youtube_fisp_arohzy8",
                "type": "Citation",
                "name": "YouTube citation",
            },
        ],
        "relationships": [
            {
                "source": "evidence_fisp_arohzy8_0001",
                "type": "HAS_CITATION",
                "target": "citation_youtube_fisp_arohzy8",
            },
            {
                "source": "evidence_fisp_arohzy8_0002",
                "type": "HAS_CITATION",
                "target": "citation_youtube_fisp_arohzy8",
            },
        ],
    }


def write_json(path: Path, payload: dict) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class BatchReviewHelperTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.input_path = self.temp_path / "evidence_batch_001.json"
        self.review_path = self.temp_path / "evidence_batch_001_review_queue.json"
        write_json(self.input_path, sample_payload())

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def init_queue(self) -> dict:
        return init_review_queue(self.input_path, self.review_path)

    def test_init_creates_review_queue(self) -> None:
        queue = self.init_queue()

        self.assertTrue(self.review_path.exists())
        self.assertEqual(len(queue["nodes"]), 3)
        self.assertEqual(queue["nodes"][0]["review_status"], "unreviewed")

    def test_init_preserves_original_evidence_text(self) -> None:
        queue = self.init_queue()
        node = queue["nodes"][0]

        self.assertEqual(node["original_evidence_text"], "Đoạn một.")
        self.assertEqual(node["reviewed_evidence_text"], "Đoạn một.")
        self.assertEqual(node["evidence_text"], "Đoạn một.")

    def test_init_does_not_duplicate_review_status(self) -> None:
        self.init_queue()
        raw_text = self.review_path.read_text(encoding="utf-8")

        def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
            keys = [key for key, _value in pairs]
            if len(keys) != len(set(keys)):
                raise ValueError("duplicate key found")
            return dict(pairs)

        json.loads(raw_text, object_pairs_hook=reject_duplicate_keys)

    def test_list_command_works(self) -> None:
        self.init_queue()

        output = list_review_queue(self.review_path)

        self.assertIn("evidence_fisp_arohzy8_0001", output)
        self.assertIn("unreviewed", output)

    def test_show_command_works(self) -> None:
        self.init_queue()

        output = show_evidence(self.review_path, "evidence_fisp_arohzy8_0001")

        self.assertIn("original_evidence_text: Đoạn một.", output)
        self.assertIn("source_url: https://www.youtube.com/watch?v=FISpARohzy8", output)

    def test_approve_marks_human_reviewed(self) -> None:
        self.init_queue()

        node = approve_evidence(
            self.review_path,
            "evidence_fisp_arohzy8_0001",
            reviewer="Minh",
            reviewed_at="2026-07-03T10:00:00+07:00",
        )

        self.assertEqual(node["review_status"], "human_reviewed")
        self.assertEqual(node["reviewer"], "Minh")
        self.assertEqual(node["review_notes"], "Approved without text changes.")
        self.assertEqual(node["reviewed_evidence_text"], "Đoạn một.")

    def test_edit_updates_reviewed_evidence_text(self) -> None:
        self.init_queue()

        node = edit_evidence(
            self.review_path,
            "evidence_fisp_arohzy8_0001",
            reviewed_text="Đoạn một đã sửa.",
            reviewer="Minh",
            notes="Sửa dấu câu.",
            reviewed_at="2026-07-03T10:00:00+07:00",
        )

        self.assertEqual(node["review_status"], "human_reviewed")
        self.assertEqual(node["reviewed_evidence_text"], "Đoạn một đã sửa.")
        self.assertEqual(node["review_notes"], "Sửa dấu câu.")

    def test_reject_marks_rejected(self) -> None:
        self.init_queue()

        node = reject_evidence(
            self.review_path,
            "evidence_fisp_arohzy8_0001",
            reviewer="Minh",
            notes="Caption quá vỡ.",
            reviewed_at="2026-07-03T10:00:00+07:00",
        )

        self.assertEqual(node["review_status"], "rejected")
        self.assertEqual(node["reviewer"], "Minh")
        self.assertEqual(node["review_notes"], "Caption quá vỡ.")

    def test_stats_counts_statuses(self) -> None:
        self.init_queue()
        approve_evidence(
            self.review_path,
            "evidence_fisp_arohzy8_0001",
            reviewer="Minh",
            reviewed_at="2026-07-03T10:00:00+07:00",
        )
        reject_evidence(
            self.review_path,
            "evidence_fisp_arohzy8_0002",
            reviewer="Minh",
            reviewed_at="2026-07-03T10:00:00+07:00",
        )

        counts = review_stats(load_json(self.review_path))

        self.assertEqual(counts["total"], 2)
        self.assertEqual(counts["human_reviewed"], 1)
        self.assertEqual(counts["rejected"], 1)
        self.assertEqual(counts["unreviewed"], 0)

    def test_cli_list_and_stats_work(self) -> None:
        self.init_queue()
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            main(["list", "--path", str(self.review_path)])
            main(["stats", "--path", str(self.review_path)])

        output = stdout.getvalue()
        self.assertIn("evidence_fisp_arohzy8_0001", output)
        self.assertIn("total Evidence: 2", output)

    def test_promotion_skips_rejected_evidence(self) -> None:
        self.init_queue()
        approve_evidence(
            self.review_path,
            "evidence_fisp_arohzy8_0001",
            reviewer="Minh",
            reviewed_at="2026-07-03T10:00:00+07:00",
        )
        reject_evidence(
            self.review_path,
            "evidence_fisp_arohzy8_0002",
            reviewer="Minh",
            reviewed_at="2026-07-03T10:00:00+07:00",
        )
        output_path = self.temp_path / "evidence_batch_001_curated.json"

        curated = promote_reviewed_evidence_file(self.review_path, output_path)

        self.assertEqual(
            [node["id"] for node in curated["nodes"]],
            ["evidence_fisp_arohzy8_0001"],
        )
        self.assertNotIn("evidence_fisp_arohzy8_0002", output_path.read_text())

    def test_promotion_accepts_custom_input_and_output(self) -> None:
        self.init_queue()
        approve_evidence(
            self.review_path,
            "evidence_fisp_arohzy8_0001",
            reviewer="Minh",
            reviewed_at="2026-07-03T10:00:00+07:00",
        )
        output_path = self.temp_path / "custom_curated.json"

        promote_reviewed_evidence_file(self.review_path, output_path)
        written = load_json(output_path)

        self.assertTrue(output_path.exists())
        self.assertEqual(written["nodes"][0]["curated_status"], "curated")

    def test_promotion_cli_accepts_input_and_output_options(self) -> None:
        self.init_queue()
        approve_evidence(
            self.review_path,
            "evidence_fisp_arohzy8_0001",
            reviewer="Minh",
            reviewed_at="2026-07-03T10:00:00+07:00",
        )
        output_path = self.temp_path / "cli_curated.json"
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            exit_code = promote_main(
                [
                    "--input",
                    str(self.review_path),
                    "--output",
                    str(output_path),
                ]
            )

        self.assertEqual(exit_code, 0)
        self.assertTrue(output_path.exists())
        self.assertIn("with 1 Evidence node", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
