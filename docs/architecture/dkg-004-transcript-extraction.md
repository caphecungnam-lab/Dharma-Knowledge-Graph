# DKG-004: Transcript Extraction Pilot

DKG-004 prepares a safe manual transcript extraction path for the Giác Khang
video `FISpARohzy8`.

## Purpose

The purpose of this step is to prepare the repository for real transcript
Evidence without adding transcript text yet.

DKG-004 adds:

- a raw input folder for the source video;
- a manual transcript JSON template;
- an importer for converting reviewed transcript segments into Evidence nodes;
- tests that reject empty or incomplete transcript segments.

The importer is intentionally conservative. It should only convert segments
that contain exact transcript text and required timing metadata.

## Source

- YouTube URL: `https://www.youtube.com/watch?v=FISpARohzy8`
- Video ID: `FISpARohzy8`
- Title: `1A. KINH 6 6 L2CÂU 1 P1`
- Speaker: `HT. Thích Giác Khang`
- Topic: `Kinh Sáu Sáu`

## No Fabricated Transcript Rule

Do not invent transcript text.

The manual template contains an empty `text` field by design. That file is only
a worksheet for future manual capture.

A segment cannot become Evidence until `text` contains exact transcript text
from the source video. Paraphrases, summaries, and guessed wording are not valid
for this transcript extraction pilot.

## Manual Input Shape

Manual transcript files live under:

```text
data/raw/giac_khang/FISpARohzy8/
```

The top-level transcript JSON must include:

- `source_url`
- `video_id`
- `title`
- `speaker`
- `language`
- `segments`

Each segment must include:

- `start_time`
- `end_time`
- `text`
- `review_status`

## Evidence Conversion

Each valid segment becomes one Evidence node.

Generated Evidence fields include:

- `id`, such as `evidence_fisp_arohzy8_0001`
- `type: Evidence`
- `name`
- `evidence_text`
- `evidence_type: transcript_excerpt`
- `language: vi`
- `confidence: low`
- `source_kind: youtube`
- `source_url`
- `document_id: document_transcript_fisp_arohzy8`
- `start_time`
- `end_time`
- `speaker`
- `review_status`
- `notes`

The importer also links each Evidence node to:

- `document_transcript_fisp_arohzy8`
- `source_youtube_fisp_arohzy8`
- `citation_youtube_fisp_arohzy8`

## Validation Rules

The importer rejects transcript files when required top-level fields are
missing or empty.

The importer rejects any segment that is missing:

- `start_time`
- `end_time`
- `text`
- `review_status`

The importer also rejects empty `text` when converting a segment into Evidence.
This prevents placeholder template rows from becoming fake Evidence.

Multiple valid segments receive stable sequential IDs:

- `evidence_fisp_arohzy8_0001`
- `evidence_fisp_arohzy8_0002`
- `evidence_fisp_arohzy8_0003`

## Next Step

The next step is manual transcript capture.

Fill `data/raw/giac_khang/FISpARohzy8/transcript_manual_template.json` with a
small number of exact transcript excerpts and timestamps. After review, run the
importer to generate an Evidence seed fragment for inspection.
