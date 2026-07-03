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
