from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from vtt_to_evidence import (  # noqa: E402
    convert_vtt_to_evidence,
    parse_timestamp_line,
    parse_vtt_segments,
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

00:00:04.000 --> 00:00:05.000
đoạn bốn

00:00:05.000 --> 00:00:06.000
đoạn năm

00:00:06.000 --> 00:00:07.000
đoạn sáu
"""


class VttToEvidenceTest(unittest.TestCase):
    def test_parses_vtt_timestamps(self) -> None:
        parsed = parse_timestamp_line("00:01:18.720 --> 00:01:21.590 align:start")

        self.assertEqual(parsed, ("00:01:18.720", "00:01:21.590"))

    def test_removes_webvtt_header(self) -> None:
        segments = parse_vtt_segments(SAMPLE_VTT)

        self.assertEqual(segments[0]["text"], "Xin chào")
        self.assertNotIn("WEBVTT", segments[0]["text"])

    def test_cleans_html_tags(self) -> None:
        segments = parse_vtt_segments(SAMPLE_VTT)

        self.assertEqual(segments[1]["text"], "thế giới")

    def test_skips_empty_captions(self) -> None:
        segments = parse_vtt_segments(SAMPLE_VTT)

        self.assertEqual(
            [segment["text"] for segment in segments],
            [
                "Xin chào",
                "thế giới",
                "đoạn ba",
                "đoạn bốn",
                "đoạn năm",
                "đoạn sáu",
            ],
        )

    def test_creates_5_evidence_nodes(self) -> None:
        output = convert_vtt_to_evidence(SAMPLE_VTT)

        self.assertEqual(len(output["nodes"]), 5)

    def test_generates_stable_ids(self) -> None:
        output = convert_vtt_to_evidence(SAMPLE_VTT)

        self.assertEqual(
            [node["id"] for node in output["nodes"]],
            [
                "evidence_fisp_arohzy8_0001",
                "evidence_fisp_arohzy8_0002",
                "evidence_fisp_arohzy8_0003",
                "evidence_fisp_arohzy8_0004",
                "evidence_fisp_arohzy8_0005",
            ],
        )


if __name__ == "__main__":
    unittest.main()
