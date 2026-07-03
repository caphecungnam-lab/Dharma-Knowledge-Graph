from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dharma_kg.citations import (  # noqa: E402
    build_citation_label,
    build_youtube_timestamp_url,
    extract_youtube_video_id,
    is_youtube_url,
    parse_time_to_seconds,
)


class CitationHelpersTest(unittest.TestCase):
    def test_parses_full_timestamp_with_milliseconds(self) -> None:
        self.assertEqual(parse_time_to_seconds("00:02:37.959"), 157)

    def test_parses_full_timestamp_without_milliseconds(self) -> None:
        self.assertEqual(parse_time_to_seconds("00:02:37"), 157)

    def test_parses_minute_second_timestamp(self) -> None:
        self.assertEqual(parse_time_to_seconds("02:37"), 157)

    def test_parses_plain_seconds(self) -> None:
        self.assertEqual(parse_time_to_seconds("157"), 157)

    def test_detects_youtube_watch_url(self) -> None:
        self.assertTrue(is_youtube_url("https://www.youtube.com/watch?v=FISpARohzy8"))

    def test_detects_youtu_be_url(self) -> None:
        self.assertTrue(is_youtube_url("https://youtu.be/FISpARohzy8"))

    def test_detects_embed_url(self) -> None:
        self.assertTrue(is_youtube_url("https://www.youtube.com/embed/FISpARohzy8"))

    def test_extracts_youtube_video_id(self) -> None:
        self.assertEqual(
            extract_youtube_video_id("https://www.youtube.com/embed/FISpARohzy8"),
            "FISpARohzy8",
        )

    def test_builds_timestamp_url_from_watch_url(self) -> None:
        self.assertEqual(
            build_youtube_timestamp_url(
                "https://www.youtube.com/watch?v=FISpARohzy8",
                "00:02:37.959",
            ),
            "https://www.youtube.com/watch?v=FISpARohzy8&t=157s",
        )

    def test_builds_timestamp_url_from_youtu_be_url(self) -> None:
        self.assertEqual(
            build_youtube_timestamp_url(
                "https://youtu.be/FISpARohzy8",
                "02:37",
            ),
            "https://www.youtube.com/watch?v=FISpARohzy8&t=157s",
        )

    def test_returns_none_for_non_youtube_url(self) -> None:
        self.assertIsNone(
            build_youtube_timestamp_url("https://example.com/video", "02:37")
        )

    def test_returns_none_for_invalid_time(self) -> None:
        self.assertIsNone(
            build_youtube_timestamp_url(
                "https://www.youtube.com/watch?v=FISpARohzy8",
                "not a timestamp",
            )
        )

    def test_builds_citation_label(self) -> None:
        self.assertEqual(
            build_citation_label("FISpARohzy8", "00:02:37.959", "00:02:54.470"),
            "FISpARohzy8 | 00:02:37.959 -> 00:02:54.470",
        )


if __name__ == "__main__":
    unittest.main()
