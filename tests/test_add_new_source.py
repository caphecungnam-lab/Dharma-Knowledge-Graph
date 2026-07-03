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
sys.path.insert(0, str(ROOT / "src"))

from add_new_source import add_youtube_source, main, parse_args  # noqa: E402
from dharma_kg.youtube import extract_youtube_video_id  # noqa: E402


def registry_payload() -> dict:
    return {
        "metadata": {
            "registry_name": "dkg_source_registry",
            "version": 1,
            "updated_at": "2026-07-03T14:30:00+07:00",
        },
        "sources": [
            {
                "source_id": "source_youtube_existing",
                "corpus_id": "corpus_giac_khang",
                "title": "Existing",
                "speaker": "HT. Thích Giác Khang",
                "source_owner": "PHÁP ÂM SƯ KHANG",
                "source_kind": "youtube",
                "source_url": "https://www.youtube.com/watch?v=existing",
                "video_id": "existing",
                "language": "vi",
                "topic": "Existing topic",
                "status": "planned",
                "ingestion_status": "pending",
                "review_status": "not_started",
                "curation_status": "not_started",
                "index_status": "not_indexed",
                "health_status": "unknown",
                "raw_paths": [],
                "processed_paths": [],
                "reviewed_paths": [],
                "curated_paths": [],
                "index_paths": [],
                "notes": "",
                "created_at": "2026-07-03T14:30:00+07:00",
                "updated_at": "2026-07-03T14:30:00+07:00",
            }
        ],
    }


def write_json(path: Path, payload: dict) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


class AddNewSourceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.registry_path = self.root / "sources.json"
        write_json(self.registry_path, registry_payload())

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def args(self, *extra: str) -> list[str]:
        return [
            "youtube",
            "--url",
            "https://www.youtube.com/watch?v=NewVideo123&si=abc",
            "--title",
            "New source title",
            "--speaker",
            "HT. Thích Giác Khang",
            "--topic",
            "New topic",
            "--registry-path",
            str(self.registry_path),
            "--base-raw-dir",
            str(self.root / "raw"),
            "--base-processed-dir",
            str(self.root / "processed"),
            "--base-reviewed-dir",
            str(self.root / "reviewed"),
            "--base-curated-dir",
            str(self.root / "curated"),
            *extra,
        ]

    def test_extracts_video_id_from_watch_url(self) -> None:
        self.assertEqual(
            extract_youtube_video_id("https://www.youtube.com/watch?v=NEW_VIDEO_ID"),
            "NEW_VIDEO_ID",
        )

    def test_extracts_video_id_from_youtu_be_url(self) -> None:
        self.assertEqual(
            extract_youtube_video_id("https://youtu.be/NEW_VIDEO_ID"),
            "NEW_VIDEO_ID",
        )

    def test_extracts_video_id_from_embed_url(self) -> None:
        self.assertEqual(
            extract_youtube_video_id("https://www.youtube.com/embed/NEW_VIDEO_ID"),
            "NEW_VIDEO_ID",
        )

    def test_dry_run_does_not_write_files(self) -> None:
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            exit_code = main(self.args("--dry-run"))

        self.assertEqual(exit_code, 0)
        self.assertIn("DRY RUN", stdout.getvalue())
        self.assertFalse((self.root / "raw" / "NewVideo123").exists())
        parsed = json.loads(self.registry_path.read_text(encoding="utf-8"))
        self.assertEqual(len(parsed["sources"]), 1)

    def test_creates_folder_scaffold_and_readmes(self) -> None:
        add_youtube_source(parse_args(self.args()))

        for folder in ["raw", "processed", "reviewed", "curated"]:
            readme = self.root / folder / "NewVideo123" / "README.md"
            self.assertTrue(readme.exists())
            self.assertIn("Source Workspace", readme.read_text(encoding="utf-8"))

    def test_adds_source_to_registry(self) -> None:
        add_youtube_source(parse_args(self.args()))
        parsed = json.loads(self.registry_path.read_text(encoding="utf-8"))
        source = parsed["sources"][1]

        self.assertEqual(source["source_id"], "source_youtube_newvideo123")
        self.assertEqual(source["video_id"], "NewVideo123")
        self.assertEqual(
            source["source_url"],
            "https://www.youtube.com/watch?v=NewVideo123",
        )
        self.assertEqual(source["status"], "planned")
        self.assertEqual(
            source["raw_paths"], [f"{self.root.as_posix()}/raw/NewVideo123/"]
        )

    def test_rejects_duplicate_source_id(self) -> None:
        with self.assertRaises(ValueError):
            add_youtube_source(
                parse_args(
                    [
                        "youtube",
                        "--url",
                        "https://www.youtube.com/watch?v=existing",
                        "--title",
                        "Existing",
                        "--speaker",
                        "HT. Thích Giác Khang",
                        "--topic",
                        "Existing topic",
                        "--registry-path",
                        str(self.registry_path),
                    ]
                )
            )

    def test_rejects_duplicate_video_id_by_default(self) -> None:
        parsed = json.loads(self.registry_path.read_text(encoding="utf-8"))
        parsed["sources"][0]["source_id"] = "source_youtube_other"
        write_json(self.registry_path, parsed)

        with self.assertRaises(ValueError):
            add_youtube_source(
                parse_args(
                    [
                        "youtube",
                        "--url",
                        "https://www.youtube.com/watch?v=existing",
                        "--title",
                        "Existing",
                        "--speaker",
                        "HT. Thích Giác Khang",
                        "--topic",
                        "Existing topic",
                        "--registry-path",
                        str(self.registry_path),
                    ]
                )
            )

    def test_allows_duplicate_video_id_when_requested(self) -> None:
        parsed = json.loads(self.registry_path.read_text(encoding="utf-8"))
        parsed["sources"][0]["source_id"] = "source_youtube_other"
        write_json(self.registry_path, parsed)

        source_entry, _output = add_youtube_source(
            parse_args(
                [
                    "youtube",
                    "--url",
                    "https://www.youtube.com/watch?v=existing",
                    "--title",
                    "Existing",
                    "--speaker",
                    "HT. Thích Giác Khang",
                    "--topic",
                    "Existing topic",
                    "--registry-path",
                    str(self.registry_path),
                    "--base-raw-dir",
                    str(self.root / "raw"),
                    "--base-processed-dir",
                    str(self.root / "processed"),
                    "--base-reviewed-dir",
                    str(self.root / "reviewed"),
                    "--base-curated-dir",
                    str(self.root / "curated"),
                    "--allow-duplicate-video-id",
                ]
            )
        )

        self.assertEqual(source_entry["video_id"], "existing")

    def test_prints_next_commands(self) -> None:
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            main(self.args("--dry-run"))

        output = stdout.getvalue()
        self.assertIn("Download transcript to:", output)
        self.assertIn("scripts/vtt_to_evidence.py", output)
        self.assertIn("scripts/batch_review_helper.py init", output)


if __name__ == "__main__":
    unittest.main()
