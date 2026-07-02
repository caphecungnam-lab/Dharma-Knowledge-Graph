# DKG-004: Transcript Extraction Pilot

DKG-004 prepares the project to convert manually reviewed transcript excerpts
from the Giác Khang video `FISpARohzy8` into Evidence nodes.

## Purpose

The goal is to create a safe transcript intake path before adding any real
transcript content to the graph.

This step provides:

- a raw input folder for the source video;
- a manual transcript JSON template;
- an importer that converts non-empty transcript segments into Evidence nodes;
- tests proving that empty or incomplete transcript segments are rejected.

## Source

- YouTube URL: `https://www.youtube.com/watch?v=FISpARohzy8`
- Video ID: `FISpARohzy8`
- Title: `1A. KINH 6 6 L2CÂU 1 P1`
- Speaker: `HT. Thích Giác Khang`
- Topic: `Kinh Sáu Sáu`

## No Fabricated Transcript Rule

Do not invent transcript text.

The manual template intentionally contains an empty `text` field. That template
is valid as a capture worksheet, but it cannot be converted into Evidence until
the field contains exact transcript text from the source video.

## Manual Input Shape

Manual transcript files live under:

```text
data/raw/giac_khang/FISpARohzy8/
```

Each segment must include:

- `start_time`
- `end_time`
- `text`
- `review_status`

The transcript file must also provide a usable `source_url`, either at the file
level or on each segment.

## Evidence Conversion

Only non-empty segment text can become Evidence.

Each converted segment becomes an Evidence node with:

- `evidence_type: transcript_excerpt`
- `confidence: low`
- `source_kind: youtube`
- `speaker: HT. Thích Giác Khang`
- a stable ID such as `evidence_fisp_arohzy8_0001`

The importer attaches each Evidence node to:

- `document_transcript_fisp_arohzy8`
- `source_youtube_fisp_arohzy8`
- `citation_youtube_fisp_arohzy8`

## Expected Output

The importer returns a seed-style JSON object with `nodes` and `relationships`.
The output should only be committed after the transcript excerpt text has been
checked and the review status is appropriate.
