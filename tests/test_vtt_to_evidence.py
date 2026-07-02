from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from vtt_to_evidence import (  # noqa: E402
    clean_caption_text,
    convert_vtt_to_evidence,
    dedupe_adjacent_text,
    format_timestamp,
    merge_cues,
    parse_timestamp_line,
    parse_vtt_segments,
    parse_vtt_timestamp,
)

SAMPLE_VTT = """WEBVTT
Kind: captions
Language: vi

00:00:00.000 --> 00:00:01.000 align:start position:0%
 
<c>Xin</c> chào

00:00:01.000 --> 00:00:02.000
<00:00:01.200><c>thế</c> giới

00:00:02.000 --> 00:00:03.000
 

00:00:03.000 --> 00:00:04.000
đoạn ba
"""

SHORT_OVERLAPPING_CUES = [
    {
        "start_time": "00:00:00.000",
        "end_time": "00:00:00.010",
        "text": "Tiếp tục bài kinh 66",
    },
    {
        "start_time": "00:00:00.010",
        "end_time": "00:00:03.000",
        "text": "Tiếp tục bài kinh 66",
    },
    {
        "start_time": "00:00:03.000",
        "end_time": "00:00:08.000",
        "text": "Tiếp tục bài kinh 66 thì trước tiên",
    },
    {
        "start_time": "00:00:08.000",
        "end_time": "00:00:12.000",
        "text": "thì trước tiên tôi xin tóm trước phần.",
    },
]

MANY_WINDOWS_VTT = """WEBVTT

00:00:00.000 --> 00:00:21.000
đoạn một về sáu căn đã xong.

00:00:21.000 --> 00:00:42.000
đoạn hai về sáu trần đã xong.

00:00:42.000 --> 00:01:03.000
đoạn ba về sáu thức đã xong.

00:01:03.000 --> 00:01:24.000
đoạn bốn giữ nguyên tiếng Việt.

00:01:24.000 --> 00:01:45.000
đoạn năm giữ nguyên nội dung.

00:01:45.000 --> 00:02:06.000
đoạn sáu không nên xuất hiện.
"""


class VttToEvidenceTest(unittest.TestCase):
    def test_parses_vtt_timestamps(self) -> None:
        parsed_line = parse_timestamp_line("00:01:18.720 --> 00:01:21.590 align:start")

        self.assertEqual(parsed_line, ("00:01:18.720", "00:01:21.590"))
        self.assertEqual(parse_vtt_timestamp("00:01:18.720"), 78.72)
        self.assertEqual(format_timestamp(78.72), "00:01:18.720")

    def test_removes_webvtt_header(self) -> None:
        segments = parse_vtt_segments(SAMPLE_VTT)

        self.assertEqual(segments[0]["text"], "Xin chào")
        self.assertNotIn("WEBVTT", segments[0]["text"])

    def test_cleans_html_tags(self) -> None:
        text = clean_caption_text("<00:00:01.200><c>thế</c> giới")

        self.assertEqual(text, "thế giới")

    def test_skips_empty_captions(self) -> None:
        segments = parse_vtt_segments(SAMPLE_VTT)

        self.assertEqual(
            [segment["text"] for segment in segments],
            [
                "Xin chào",
                "thế giới",
                "đoạn ba",
            ],
        )

    def test_removes_duplicate_adjacent_captions(self) -> None:
        duplicate = dedupe_adjacent_text(
            "Tiếp tục bài kinh 66",
            "Tiếp tục bài kinh 66",
        )
        overlap = dedupe_adjacent_text(
            "Tiếp tục bài kinh 66",
            "Tiếp tục bài kinh 66 thì trước tiên",
        )

        self.assertEqual(duplicate, "")
        self.assertEqual(overlap, "thì trước tiên")

    def test_removes_overlap_between_merged_segments(self) -> None:
        segments = merge_cues(
            [
                {
                    "start_time": "00:00:00.000",
                    "end_time": "00:00:21.000",
                    "text": "đoạn một về sáu căn đã xong.",
                },
                {
                    "start_time": "00:00:21.000",
                    "end_time": "00:00:42.000",
                    "text": "đoạn một về sáu căn đã xong. đoạn hai tiếp tục.",
                },
            ]
        )

        self.assertEqual(len(segments), 2)
        self.assertEqual(segments[1]["text"], "đoạn hai tiếp tục.")

    def test_merges_short_cues_into_longer_evidence(self) -> None:
        segments = merge_cues(SHORT_OVERLAPPING_CUES)

        self.assertEqual(len(segments), 1)
        self.assertEqual(
            segments[0]["text"],
            "Tiếp tục bài kinh 66 thì trước tiên tôi xin tóm trước phần.",
        )

    def test_does_not_create_001_second_evidence(self) -> None:
        output = convert_vtt_to_evidence("""WEBVTT

00:00:00.000 --> 00:00:00.010
Tiếp tục bài kinh 66

00:00:00.010 --> 00:00:03.000
Tiếp tục bài kinh 66

00:00:03.000 --> 00:00:08.000
Tiếp tục bài kinh 66 thì trước tiên

00:00:08.000 --> 00:00:12.000
thì trước tiên tôi xin tóm trước phần.
""")

        self.assertEqual(len(output["nodes"]), 1)
        node = output["nodes"][0]
        duration = parse_vtt_timestamp(node["end_time"]) - parse_vtt_timestamp(
            node["start_time"]
        )
        self.assertGreaterEqual(duration, 5)

    def test_keeps_first_start_time_and_last_end_time(self) -> None:
        segments = merge_cues(SHORT_OVERLAPPING_CUES)

        self.assertEqual(segments[0]["start_time"], "00:00:00.000")
        self.assertEqual(segments[0]["end_time"], "00:00:12.000")

    def test_creates_at_most_5_evidence_nodes(self) -> None:
        output = convert_vtt_to_evidence(MANY_WINDOWS_VTT)

        self.assertEqual(len(output["nodes"]), 5)
        self.assertEqual(output["nodes"][-1]["id"], "evidence_fisp_arohzy8_0005")

    def test_preserves_vietnamese_unicode(self) -> None:
        output = convert_vtt_to_evidence(MANY_WINDOWS_VTT)

        self.assertIn("sáu căn", output["nodes"][0]["evidence_text"])
        self.assertIn("tiếng Việt", output["nodes"][3]["evidence_text"])


if __name__ == "__main__":
    unittest.main()
