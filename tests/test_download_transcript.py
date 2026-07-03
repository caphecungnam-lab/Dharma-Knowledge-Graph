from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

import download_transcript as downloader  # noqa: E402


def source_record(**overrides: object) -> dict:
    source = {
        "source_id": "source_youtube_fisp_arohzy8",
        "corpus_id": "corpus_giac_khang",
        "title": "1A. KINH 6 6 L2CÂU 1 P1",
        "speaker": "HT. Thích Giác Khang",
        "source_owner": "PHÁP ÂM SƯ KHANG",
        "source_kind": "youtube",
        "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
        "video_id": "FISpARohzy8",
        "language": "vi",
        "topic": "Kinh Sáu Sáu",
        "status": "pilot",
        "ingestion_status": "ingested",
        "review_status": "partially_reviewed",
        "curation_status": "partially_curated",
        "index_status": "indexed",
        "health_status": "pass",
        "raw_paths": [],
        "processed_paths": [],
        "reviewed_paths": [],
        "curated_paths": [],
        "index_paths": [],
        "notes": "Initial Giac Khang pilot source.",
        "created_at": "2026-07-03T14:30:00+07:00",
        "updated_at": "2026-07-03T14:30:00+07:00",
    }
    source.update(overrides)
    return source


def registry_payload(sources: list[dict] | None = None) -> dict:
    return {
        "metadata": {
            "registry_name": "dkg_source_registry",
            "version": 1,
            "updated_at": "2026-07-03T14:30:00+07:00",
        },
        "sources": sources if sources is not None else [source_record()],
    }


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def completed(command: list[str], returncode: int = 0) -> subprocess.CompletedProcess:
    return subprocess.CompletedProcess(
        args=command,
        returncode=returncode,
        stdout="",
        stderr="" if returncode == 0 else "download failed",
    )


class DownloadTranscriptTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.registry_path = self.root / "registry" / "sources.json"
        write_json(self.registry_path, registry_payload())

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def output_path(self, name: str = "source.vi.vtt") -> Path:
        return self.root / "raw" / "FISpARohzy8" / name

    def fake_run_with_vtt(self, command: list[str]) -> subprocess.CompletedProcess:
        output_index = command.index("--output") + 1
        temp_dir = Path(command[output_index]).parent
        temp_dir.mkdir(parents=True, exist_ok=True)
        (temp_dir / "FISpARohzy8.vi.vtt").write_text(
            "WEBVTT\n\n00:00:00.000 --> 00:00:02.000\nXin chào\n",
            encoding="utf-8",
        )
        return completed(command)

    def test_resolves_output_path_from_source_id(self) -> None:
        result = downloader.download_transcript(
            "source_youtube_fisp_arohzy8",
            registry_path=self.registry_path,
            dry_run=True,
        )

        self.assertEqual(
            result["output"],
            "data/raw/giac_khang/FISpARohzy8/source.vi.vtt",
        )

    def test_fails_if_source_id_missing(self) -> None:
        with self.assertRaisesRegex(ValueError, "Source not found"):
            downloader.download_transcript(
                "source_youtube_missing",
                registry_path=self.registry_path,
                dry_run=True,
            )

    def test_fails_if_source_kind_is_not_youtube(self) -> None:
        write_json(
            self.registry_path,
            registry_payload([source_record(source_kind="book")]),
        )

        with self.assertRaisesRegex(ValueError, "not youtube"):
            downloader.download_transcript(
                "source_youtube_fisp_arohzy8",
                registry_path=self.registry_path,
                dry_run=True,
            )

    def test_fails_if_output_exists_without_force(self) -> None:
        output = self.output_path()
        output.parent.mkdir(parents=True)
        output.write_text("existing", encoding="utf-8")

        with self.assertRaisesRegex(FileExistsError, "already exists"):
            downloader.download_transcript(
                "source_youtube_fisp_arohzy8",
                registry_path=self.registry_path,
                output=output,
            )

    def test_dry_run_does_not_call_subprocess(self) -> None:
        with patch.object(downloader, "run_command") as run_command:
            result = downloader.download_transcript(
                "source_youtube_fisp_arohzy8",
                registry_path=self.registry_path,
                output=self.output_path(),
                dry_run=True,
            )

        self.assertTrue(result["dry_run"])
        run_command.assert_not_called()

    def test_builds_yt_dlp_command(self) -> None:
        command = downloader.build_yt_dlp_command(
            ["python3", "-m", "yt_dlp"],
            "https://www.youtube.com/watch?v=FISpARohzy8",
            "vi",
            self.root / ".tmp_download",
        )

        self.assertIn("--skip-download", command)
        self.assertIn("--write-auto-subs", command)
        self.assertIn("--sub-lang", command)
        self.assertIn("vi", command)
        self.assertEqual(command[-1], "https://www.youtube.com/watch?v=FISpARohzy8")

    def test_builds_command_with_no_check_certificates(self) -> None:
        command = downloader.build_yt_dlp_command(
            ["python3", "-m", "yt_dlp"],
            "https://www.youtube.com/watch?v=FISpARohzy8",
            "vi",
            self.root / ".tmp_download",
            no_check_certificates=True,
        )

        self.assertIn("--no-check-certificates", command)

    def test_update_registry_adds_raw_path_after_success(self) -> None:
        output = self.output_path()

        with (
            patch.object(
                downloader,
                "detect_yt_dlp_command",
                return_value=["python3", "-m", "yt_dlp"],
            ),
            patch.object(downloader, "run_command", side_effect=self.fake_run_with_vtt),
        ):
            result = downloader.download_transcript(
                "source_youtube_fisp_arohzy8",
                registry_path=self.registry_path,
                output=output,
                update_registry=True,
            )

        parsed = json.loads(self.registry_path.read_text(encoding="utf-8"))
        source = parsed["sources"][0]
        self.assertEqual(result["output"], output.as_posix())
        self.assertTrue(output.exists())
        self.assertEqual(source["ingestion_status"], "transcript_downloaded")
        self.assertIn(output.as_posix(), source["raw_paths"])

    def test_does_not_update_registry_on_failed_download(self) -> None:
        output = self.output_path()

        with (
            patch.object(
                downloader,
                "detect_yt_dlp_command",
                return_value=["python3", "-m", "yt_dlp"],
            ),
            patch.object(
                downloader,
                "run_command",
                return_value=completed(["python3", "-m", "yt_dlp"], returncode=1),
            ),
        ):
            with self.assertRaisesRegex(RuntimeError, "Transcript download failed"):
                downloader.download_transcript(
                    "source_youtube_fisp_arohzy8",
                    registry_path=self.registry_path,
                    output=output,
                    update_registry=True,
                )

        parsed = json.loads(self.registry_path.read_text(encoding="utf-8"))
        source = parsed["sources"][0]
        self.assertEqual(source["ingestion_status"], "ingested")
        self.assertEqual(source["raw_paths"], [])

    def test_handles_missing_yt_dlp_with_clear_error(self) -> None:
        with (
            patch.object(
                downloader,
                "run_command",
                return_value=completed(["python3", "-m", "yt_dlp"], returncode=1),
            ),
            patch.object(shutil, "which", return_value=None),
        ):
            with self.assertRaisesRegex(RuntimeError, "python3 -m pip install yt-dlp"):
                downloader.detect_yt_dlp_command()

    def test_fallback_language_is_reported(self) -> None:
        output = self.output_path()
        calls: list[str] = []

        def fake_run(command: list[str]) -> subprocess.CompletedProcess:
            language = command[command.index("--sub-lang") + 1]
            calls.append(language)
            if language == "vi":
                return completed(command, returncode=1)
            return self.fake_run_with_vtt(command)

        with (
            patch.object(
                downloader,
                "detect_yt_dlp_command",
                return_value=["python3", "-m", "yt_dlp"],
            ),
            patch.object(downloader, "run_command", side_effect=fake_run),
        ):
            result = downloader.download_transcript(
                "source_youtube_fisp_arohzy8",
                registry_path=self.registry_path,
                output=output,
            )

        self.assertEqual(calls[:2], ["vi", "vi-orig"])
        self.assertEqual(result["downloaded_language"], "vi-orig")


if __name__ == "__main__":
    unittest.main()
