import json

from dharma_kg import source_pipeline as sp
from dharma_kg.source_pipeline import detect_source_type


def test_detect_youtube_source():
    assert detect_source_type("https://youtube.com/watch?v=abc") == "youtube"
    assert detect_source_type("https://youtu.be/abc") == "youtube"


def test_detect_text_source():
    assert detect_source_type("lesson.txt") == "text"


def test_detect_markdown_source():
    assert detect_source_type("note.md") == "markdown"


def test_detect_json_source():
    assert detect_source_type("data/source.json") == "json"


def test_detect_web_source():
    assert detect_source_type("https://example.com/page") == "web"


def test_detect_local_source():
    assert detect_source_type("data/raw/source") == "local"


def test_load_existing_source_manifest(tmp_path, monkeypatch):
    sources_dir = tmp_path / "sources"
    sources_dir.mkdir()
    manifest = sources_dir / "a.json"
    manifest.write_text(
        json.dumps(
            {
                "id": "a",
                "teacher": "giac_khang",
                "source": "same-source",
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(sp, "SOURCES_DIR", sources_dir)

    assert sp.load_existing_source_manifest("same-source", "giac_khang") == manifest
    assert sp.load_existing_source_manifest("same-source", "other") is None


def test_load_existing_source_manifest_ignores_broken_json(tmp_path, monkeypatch):
    sources_dir = tmp_path / "sources"
    sources_dir.mkdir()
    broken = sources_dir / "broken.json"
    broken.write_text("{", encoding="utf-8")
    manifest = sources_dir / "valid.json"
    manifest.write_text(
        json.dumps(
            {
                "id": "valid",
                "teacher": "giac_khang",
                "source": "same-source",
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(sp, "SOURCES_DIR", sources_dir)

    assert sp.load_existing_source_manifest("same-source", "giac_khang") == manifest


def test_write_source_manifest_returns_existing_manifest(tmp_path, monkeypatch):
    sources_dir = tmp_path / "sources"
    sources_dir.mkdir()
    manifest = sources_dir / "existing.json"
    manifest.write_text(
        json.dumps(
            {
                "id": "existing",
                "teacher": "giac_khang",
                "source": "same-source",
                "status": "processed",
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(sp, "SOURCES_DIR", sources_dir)

    assert sp.write_source_manifest("same-source", "giac_khang") == manifest
    assert len(list(sources_dir.glob("*.json"))) == 1
