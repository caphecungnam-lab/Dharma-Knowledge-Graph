from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dharma_kg.youtube import (  # noqa: E402
    extract_youtube_video_id,
    normalize_youtube_url,
)


class YouTubeTest(unittest.TestCase):
    def test_extracts_video_id_from_watch_url(self) -> None:
        self.assertEqual(
            extract_youtube_video_id(
                "https://www.youtube.com/watch?v=FISpARohzy8&si=abc"
            ),
            "FISpARohzy8",
        )

    def test_extracts_video_id_from_youtu_be_url(self) -> None:
        self.assertEqual(
            extract_youtube_video_id("https://youtu.be/FISpARohzy8?si=abc"),
            "FISpARohzy8",
        )

    def test_extracts_video_id_from_embed_url(self) -> None:
        self.assertEqual(
            extract_youtube_video_id("https://www.youtube.com/embed/FISpARohzy8"),
            "FISpARohzy8",
        )

    def test_normalize_youtube_url_returns_canonical_watch_url(self) -> None:
        self.assertEqual(
            normalize_youtube_url("https://youtu.be/FISpARohzy8?si=abc"),
            "https://www.youtube.com/watch?v=FISpARohzy8",
        )

    def test_invalid_url_returns_none(self) -> None:
        self.assertIsNone(extract_youtube_video_id("https://example.com/video"))
        self.assertIsNone(normalize_youtube_url("https://example.com/video"))


if __name__ == "__main__":
    unittest.main()
