from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

from source_registry import (  # noqa: E402
    add_youtube_source,
    list_sources,
    main,
    show_source,
    validate_registry,
)
from dharma_kg.source_registry import (  # noqa: E402
    SourceRecord,
    find_record_by_id,
    save_record,
    validate_record,
)


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
        "raw_paths": ["data/raw/giac_khang/FISpARohzy8/source.vi.vtt"],
        "processed_paths": [],
        "reviewed_paths": [],
        "curated_paths": [],
        "index_paths": ["data/indexes/giac_khang/curated_evidence_index.json"],
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
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def add_args(source_id: str = "source_youtube_example") -> Namespace:
    return Namespace(
        source_id=source_id,
        video_id="example",
        url="https://www.youtube.com/watch?v=example",
        title="Example title",
        speaker="HT. Thích Giác Khang",
        source_owner="PHÁP ÂM SƯ KHANG",
        topic="Example topic",
        language="vi",
        corpus_id="corpus_giac_khang",
    )


class SourceRegistryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.path = Path(self.temp_dir.name) / "sources.json"
        write_json(self.path, registry_payload())

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_registry_file_is_valid_json(self) -> None:
        parsed = json.loads(
            (ROOT / "data" / "registry" / "sources.json").read_text(encoding="utf-8")
        )

        self.assertEqual(parsed["metadata"]["registry_name"], "dkg_source_registry")

    def test_validates_initial_source(self) -> None:
        errors = validate_registry(registry_payload())

        self.assertEqual(errors, [])

    def test_list_command_works(self) -> None:
        output = list_sources(self.path)

        self.assertIn("source_youtube_fisp_arohzy8", output)
        self.assertIn("partially_reviewed", output)

    def test_show_command_works(self) -> None:
        output = show_source("source_youtube_fisp_arohzy8", self.path)

        self.assertIn("title: 1A. KINH 6 6 L2CÂU 1 P1", output)
        self.assertIn("speaker: HT. Thích Giác Khang", output)

    def test_validate_detects_duplicate_source_id(self) -> None:
        errors = validate_registry(registry_payload([source_record(), source_record()]))

        self.assertIn("duplicate source_id", " ".join(errors))

    def test_validate_detects_missing_required_fields(self) -> None:
        errors = validate_registry(registry_payload([source_record(source_url="")]))

        self.assertIn("missing required field: source_url", " ".join(errors))

    def test_add_youtube_adds_source_with_default_statuses(self) -> None:
        add_youtube_source(add_args(), self.path)
        parsed = json.loads(self.path.read_text(encoding="utf-8"))
        added = parsed["sources"][1]

        self.assertEqual(added["source_id"], "source_youtube_example")
        self.assertEqual(added["status"], "planned")
        self.assertEqual(added["ingestion_status"], "pending")
        self.assertEqual(added["review_status"], "not_started")
        self.assertEqual(added["curation_status"], "not_started")
        self.assertEqual(added["index_status"], "not_indexed")
        self.assertEqual(added["health_status"], "unknown")

    def test_add_youtube_rejects_duplicate_source_id(self) -> None:
        with self.assertRaises(ValueError):
            add_youtube_source(add_args("source_youtube_fisp_arohzy8"), self.path)

    def test_path_fields_must_be_lists(self) -> None:
        errors = validate_registry(
            registry_payload([source_record(raw_paths="not a list")])
        )

        self.assertIn("raw_paths must be a list", " ".join(errors))

    def test_main_validate_command(self) -> None:
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            exit_code = main(["--path", str(self.path), "validate"])

        self.assertEqual(exit_code, 0)
        self.assertIn("Source Registry: PASS", stdout.getvalue())

    def test_find_record_by_id(self) -> None:
        record = SourceRecord(path=Path("source.json"), data={"id": "id1"})

        self.assertIs(find_record_by_id([record], "id1"), record)
        self.assertIsNone(find_record_by_id([record], "missing"))

    def test_save_record_writes_json(self) -> None:
        path = Path(self.temp_dir.name) / "source.json"
        record = SourceRecord(path=path, data={"id": "x", "status": "registered"})

        save_record(record)

        saved = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(saved["id"], "x")
        self.assertEqual(saved["status"], "registered")

    def test_validate_source_record_still_works(self) -> None:
        record = SourceRecord(
            path=Path("source.json"),
            data={
                "id": "giac_khang_text_001",
                "teacher": "giac_khang",
                "title": "Test",
                "source": "data/raw/test.txt",
                "source_type": "text",
                "created_at": "2026-07-03T00:00:00",
                "status": "registered",
            },
        )

        self.assertEqual(validate_record(record), [])


if __name__ == "__main__":
    unittest.main()
