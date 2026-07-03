from __future__ import annotations

import json

from dharma_kg.source_validator import (
    validate_manifest_payload,
    validate_source_type,
    validate_source_value,
    validate_teacher_namespace,
)


def valid_payload(source: str) -> dict[str, str]:
    return {
        "id": "giac_khang_text_001",
        "teacher": "giac_khang",
        "title": "Test",
        "source": source,
        "source_type": "text",
        "created_at": "2026-07-03T00:00:00",
        "status": "registered",
    }


def test_validate_teacher_namespace_valid():
    assert validate_teacher_namespace("giac_khang") == []
    assert validate_teacher_namespace("teacher1") == []
    assert validate_teacher_namespace("su_ong_2026") == []


def test_validate_teacher_namespace_invalid():
    assert validate_teacher_namespace("Giac Khang")
    assert validate_teacher_namespace("giac-khang")
    assert validate_teacher_namespace("../x")
    assert validate_teacher_namespace("abc/def")


def test_validate_source_type_valid():
    for source_type in ["youtube", "text", "markdown", "json", "web", "local"]:
        assert validate_source_type(source_type) == []


def test_validate_source_type_invalid():
    assert validate_source_type("pdf")


def test_validate_source_value_youtube():
    assert validate_source_value("https://youtube.com/watch?v=abc", "youtube") == []
    assert validate_source_value("https://youtu.be/abc", "youtube") == []
    assert "invalid youtube source" in validate_source_value(
        "https://example.com", "youtube"
    )


def test_validate_source_value_web():
    assert validate_source_value("https://example.com", "web") == []
    assert "invalid web source" in validate_source_value("ftp://example.com", "web")


def test_validate_source_value_text_with_tmp_file(tmp_path):
    source = tmp_path / "a.txt"
    source.write_text("hello", encoding="utf-8")

    assert validate_source_value(str(source), "text") == []


def test_validate_source_value_text_missing_file(tmp_path):
    source = tmp_path / "missing.txt"

    errors = validate_source_value(str(source), "text")
    assert any("not found" in error for error in errors)
    assert validate_source_value(str(source), "text", check_exists=False) == []


def test_validate_manifest_payload_valid(tmp_path):
    source = tmp_path / "a.txt"
    source.write_text("hello", encoding="utf-8")

    assert validate_manifest_payload(valid_payload(str(source))) == []


def test_validate_manifest_payload_missing_fields(tmp_path):
    payload = valid_payload(str(tmp_path / "a.txt"))
    payload.pop("source")
    payload.pop("status")

    errors = validate_manifest_payload(payload, check_exists=False)
    assert any("missing fields" in error for error in errors)


def test_validate_manifest_payload_invalid_status(tmp_path):
    payload = valid_payload(str(tmp_path / "a.txt"))
    payload["status"] = "unknown"

    assert "invalid status: unknown" in validate_manifest_payload(
        payload,
        check_exists=False,
    )


def test_validate_manifest_payload_title_can_be_empty(tmp_path):
    source = tmp_path / "a.txt"
    source.write_text("hello", encoding="utf-8")
    payload = valid_payload(str(source))
    payload["title"] = ""

    assert validate_manifest_payload(payload) == []


def test_validate_manifest_cli_payload(tmp_path):
    source = tmp_path / "a.txt"
    source.write_text("hello", encoding="utf-8")
    path = tmp_path / "manifest.json"
    path.write_text(
        json.dumps(valid_payload(str(source)), indent=2),
        encoding="utf-8",
    )

    assert validate_manifest_payload(json.loads(path.read_text(encoding="utf-8"))) == []
