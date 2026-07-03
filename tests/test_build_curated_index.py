from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_curated_index import (  # noqa: E402
    build_curated_index,
    build_curated_index_from_files,
    find_curated_files,
)


def evidence_node(
    node_id: str,
    text: str,
    start_time: str,
    curated_at: str = "2026-07-03T10:00:00+07:00",
) -> dict:
    return {
        "id": node_id,
        "type": "Evidence",
        "name": f"Evidence {node_id}",
        "evidence_text": text,
        "reviewed_evidence_text": text,
        "original_evidence_text": text,
        "document_id": "document_transcript_fisp_arohzy8",
        "start_time": start_time,
        "end_time": "00:01:39.030",
        "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
        "speaker": "HT. Thích Giác Khang",
        "review_status": "human_reviewed",
        "curated_status": "curated",
        "curated_at": curated_at,
    }


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


class BuildCuratedIndexTest(unittest.TestCase):
    def test_builds_index_from_multiple_curated_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            first = root / "video" / "evidence_curated.json"
            second = root / "video" / "evidence_batch_001_curated.json"
            write_json(
                first,
                {"nodes": [evidence_node("evidence_0001", "Một", "00:00:10.000")]},
            )
            write_json(
                second,
                {"nodes": [evidence_node("evidence_0002", "Hai", "00:00:20.000")]},
            )

            index = build_curated_index_from_files(find_curated_files(root))

            self.assertEqual(index["metadata"]["evidence_count"], 2)
            self.assertEqual(
                [node["id"] for node in index["nodes"]],
                ["evidence_0001", "evidence_0002"],
            )

    def test_deduplicates_evidence_by_id_and_prefers_newest_curated(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            older = root / "a" / "evidence_curated.json"
            newer = root / "b" / "evidence_batch_001_curated.json"
            write_json(
                older,
                {
                    "nodes": [
                        evidence_node(
                            "evidence_0001",
                            "Older text",
                            "00:00:10.000",
                            curated_at="2026-07-03T10:00:00+07:00",
                        )
                    ]
                },
            )
            write_json(
                newer,
                {
                    "nodes": [
                        evidence_node(
                            "evidence_0001",
                            "Newer text",
                            "00:00:10.000",
                            curated_at="2026-07-03T11:00:00+07:00",
                        )
                    ]
                },
            )

            index = build_curated_index_from_files(find_curated_files(root))

            self.assertEqual(index["metadata"]["evidence_count"], 1)
            self.assertEqual(index["nodes"][0]["evidence_text"], "Newer text")

    def test_sorts_evidence_deterministically(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "evidence_curated.json"
            write_json(
                path,
                {
                    "nodes": [
                        evidence_node("evidence_0003", "Ba", "00:00:30.000"),
                        evidence_node("evidence_0001", "Một", "00:00:10.000"),
                        evidence_node("evidence_0002", "Hai", "00:00:20.000"),
                    ]
                },
            )

            index = build_curated_index_from_files([path])

            self.assertEqual(
                [node["id"] for node in index["nodes"]],
                ["evidence_0001", "evidence_0002", "evidence_0003"],
            )

    def test_includes_metadata_source_files_and_evidence_count(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "evidence_curated.json"
            write_json(
                path,
                {"nodes": [evidence_node("evidence_0001", "Một", "00:00:10.000")]},
            )

            index = build_curated_index_from_files([path])

            self.assertEqual(
                index["metadata"]["index_name"],
                "giac_khang_curated_evidence_index",
            )
            self.assertEqual(index["metadata"]["corpus_id"], "corpus_giac_khang")
            self.assertEqual(index["metadata"]["evidence_count"], 1)
            self.assertEqual(index["metadata"]["source_files"], [str(path)])
            self.assertIn("generated_at", index["metadata"])

    def test_writes_valid_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            input_dir = root / "curated"
            output_path = root / "indexes" / "curated_evidence_index.json"
            write_json(
                input_dir / "video" / "evidence_curated.json",
                {
                    "nodes": [
                        evidence_node(
                            "evidence_0001",
                            "Một đoạn Evidence đủ dài.",
                            "00:00:10.000",
                        )
                    ]
                },
            )

            build_curated_index(input_dir, output_path)
            written = json.loads(output_path.read_text(encoding="utf-8"))

            self.assertEqual(written["metadata"]["evidence_count"], 1)
            self.assertEqual(written["nodes"][0]["id"], "evidence_0001")
            self.assertEqual(
                written["nodes"][0]["citation_url"],
                "https://www.youtube.com/watch?v=FISpARohzy8&t=10s",
            )
            self.assertIn("quality_score", written["nodes"][0])
            self.assertIn("quality_flags", written["nodes"][0])
            self.assertIn("has_text", written["nodes"][0]["quality_flags"])


if __name__ == "__main__":
    unittest.main()
