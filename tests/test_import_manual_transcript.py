from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from import_manual_transcript import (  # noqa: E402
    CITATION_ID,
    DOCUMENT_ID,
    SOURCE_ID,
    ManualTranscriptError,
    import_transcript_file,
)


def valid_segment(text: str = "Non-empty test transcript fixture.") -> dict:
    return {
        "start_time": "00:00:00",
        "end_time": "00:00:30",
        "text": text,
        "review_status": "unreviewed",
        "notes": "Test-only segment.",
    }


def valid_transcript(*segments: dict) -> dict:
    return {
        "source_url": "https://www.youtube.com/watch?v=FISpARohzy8",
        "video_id": "FISpARohzy8",
        "title": "1A. KINH 6 6 L2CÂU 1 P1",
        "speaker": "HT. Thích Giác Khang",
        "language": "vi",
        "segments": list(segments),
    }


def write_transcript_file(directory: Path, data: dict) -> Path:
    path = directory / "transcript.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def assert_import_fails(data: dict, message: str) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = write_transcript_file(Path(tmp), data)

        try:
            import_transcript_file(path)
        except ManualTranscriptError as exc:
            assert message in str(exc)
        else:
            raise AssertionError("import_transcript_file should have failed")


def test_valid_transcript_creates_evidence_node() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = write_transcript_file(
            Path(tmp),
            valid_transcript(valid_segment()),
        )
        converted = import_transcript_file(path)

    assert len(converted["nodes"]) == 1

    node = converted["nodes"][0]
    assert node["id"] == "evidence_fisp_arohzy8_0001"
    assert node["type"] == "Evidence"
    assert node["name"] == "Transcript excerpt 0001 from FISpARohzy8"
    assert node["evidence_text"] == "Non-empty test transcript fixture."
    assert node["evidence_type"] == "transcript_excerpt"
    assert node["language"] == "vi"
    assert node["confidence"] == "low"
    assert node["source_kind"] == "youtube"
    assert node["source_url"] == "https://www.youtube.com/watch?v=FISpARohzy8"
    assert node["document_id"] == DOCUMENT_ID
    assert node["start_time"] == "00:00:00"
    assert node["end_time"] == "00:00:30"
    assert node["speaker"] == "HT. Thích Giác Khang"
    assert node["review_status"] == "unreviewed"
    assert node["notes"] == "Test-only segment."

    assert {
        "source": DOCUMENT_ID,
        "type": "HAS_EVIDENCE",
        "target": node["id"],
    } in converted["relationships"]
    assert {
        "source": node["id"],
        "type": "DERIVED_FROM",
        "target": DOCUMENT_ID,
    } in converted["relationships"]
    assert {
        "source": node["id"],
        "type": "DERIVED_FROM",
        "target": SOURCE_ID,
    } in converted["relationships"]
    assert {
        "source": node["id"],
        "type": "HAS_CITATION",
        "target": CITATION_ID,
    } in converted["relationships"]


def test_empty_text_is_rejected() -> None:
    segment = valid_segment(text="")
    transcript = valid_transcript(segment)

    assert_import_fails(transcript, "empty text")


def test_missing_start_time_is_rejected() -> None:
    segment = valid_segment()
    del segment["start_time"]
    transcript = valid_transcript(segment)

    assert_import_fails(transcript, "missing start_time")


def test_missing_end_time_is_rejected() -> None:
    segment = valid_segment()
    del segment["end_time"]
    transcript = valid_transcript(segment)

    assert_import_fails(transcript, "missing end_time")


def test_missing_review_status_is_rejected() -> None:
    segment = valid_segment()
    del segment["review_status"]
    transcript = valid_transcript(segment)

    assert_import_fails(transcript, "missing review_status")


def test_multiple_segments_generate_stable_sequential_ids() -> None:
    first = valid_segment(text="First non-empty test fixture.")

    second = valid_segment(text="Second non-empty test fixture.")
    second["start_time"] = "00:00:31"
    second["end_time"] = "00:01:00"

    with tempfile.TemporaryDirectory() as tmp:
        path = write_transcript_file(
            Path(tmp),
            valid_transcript(first, second),
        )
        converted = import_transcript_file(path)

    assert [node["id"] for node in converted["nodes"]] == [
        "evidence_fisp_arohzy8_0001",
        "evidence_fisp_arohzy8_0002",
    ]


def load_tests(
    loader: unittest.TestLoader,
    tests: unittest.TestSuite,
    pattern: str | None,
) -> unittest.TestSuite:
    del loader, tests, pattern

    suite = unittest.TestSuite()

    for name, value in sorted(globals().items()):
        if name.startswith("test_") and callable(value):
            suite.addTest(unittest.FunctionTestCase(value))

    return suite
