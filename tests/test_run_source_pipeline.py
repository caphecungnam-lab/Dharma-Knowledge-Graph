from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

import run_source_pipeline as pipeline  # noqa: E402


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
        "ingestion_status": "transcript_downloaded",
        "review_status": "partially_reviewed",
        "curation_status": "partially_curated",
        "index_status": "indexed",
        "health_status": "pass",
        "raw_paths": [],
        "processed_paths": [],
        "reviewed_paths": [],
        "curated_paths": [],
        "index_paths": [],
        "notes": "",
        "created_at": "2026-07-03T14:30:00+07:00",
        "updated_at": "2026-07-03T14:30:00+07:00",
    }
    source.update(overrides)
    return source


def registry_payload() -> dict:
    return {
        "metadata": {
            "registry_name": "dkg_source_registry",
            "version": 1,
            "updated_at": "2026-07-03T14:30:00+07:00",
        },
        "sources": [source_record()],
    }


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


class RunSourcePipelineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.registry_path = self.root / "sources.json"
        write_json(self.registry_path, registry_payload())

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_preview_shows_pipeline_without_running_subprocess(self) -> None:
        with patch.object(pipeline.subprocess, "run") as run:
            output = pipeline.run_pipeline(
                "source_youtube_fisp_arohzy8",
                registry_path=self.registry_path,
            )

        self.assertIn("Source Pipeline: PREVIEW", output)
        self.assertIn("scripts/download_transcript.py", output)
        self.assertIn("scripts/vtt_to_evidence.py", output)
        run.assert_not_called()

    def test_missing_source_lists_available_sources(self) -> None:
        with self.assertRaisesRegex(ValueError, "source_youtube_fisp_arohzy8"):
            pipeline.run_pipeline(
                "source_youtube_missing",
                registry_path=self.registry_path,
            )

    def test_paths_are_derived_from_video_id_and_language(self) -> None:
        paths = pipeline.pipeline_paths(source_record(video_id="abc123", language="vi"))

        self.assertEqual(
            paths.raw_vtt.as_posix(),
            "data/raw/giac_khang/abc123/source.vi.vtt",
        )
        self.assertEqual(
            paths.processed_batch.as_posix(),
            "data/processed/giac_khang/abc123/evidence_batch_001.json",
        )

    def test_execute_runs_steps(self) -> None:
        completed = subprocess.CompletedProcess(args=[], returncode=0)

        with patch.object(
            pipeline.subprocess,
            "run",
            return_value=completed,
        ) as run:
            with redirect_stdout(StringIO()):
                output = pipeline.run_pipeline(
                    "source_youtube_fisp_arohzy8",
                    registry_path=self.registry_path,
                    execute=True,
                    force=True,
                )

        self.assertEqual(output, "Source pipeline complete.")
        self.assertEqual(run.call_count, 5)

    def test_execute_raises_when_step_fails(self) -> None:
        failed = subprocess.CompletedProcess(args=[], returncode=1)

        with patch.object(pipeline.subprocess, "run", return_value=failed):
            with self.assertRaisesRegex(RuntimeError, "Step failed"):
                with redirect_stdout(StringIO()):
                    pipeline.run_pipeline(
                        "source_youtube_fisp_arohzy8",
                        registry_path=self.registry_path,
                        execute=True,
                    )


if __name__ == "__main__":
    unittest.main()
