# DKG-003: Real Transcript Pilot

DKG-003 creates the first real-source transcript scaffold for the Giác Khang
Corpus. It prepares the graph for future transcript Evidence without adding any
fabricated excerpt text.

## Purpose

The purpose of this pilot is to model a real teaching source before transcript
extraction begins.

This step creates source, document, citation, concept, and term structure for a
specific YouTube video. It does not create Evidence nodes, because transcript
excerpt text and timestamps have not been imported or reviewed yet.

The pilot should make the next ingestion step clear: when a real excerpt is
available, it can be attached to the existing source and transcript document
instead of being modeled from scratch.

## Source Metadata

- YouTube URL: `https://www.youtube.com/watch?v=FISpARohzy8`
- YouTube short URL: `https://youtu.be/FISpARohzy8?si=YosdiHbc5e4rPBVc`
- YouTube video ID: `FISpARohzy8`
- Title: `1A. KINH 6 6 L2CÂU 1 P1`
- Speaker: `HT. Thích Giác Khang`
- Channel: `PHÁP ÂM SƯ KHANG`
- Topic: `Kinh Sáu Sáu`
- Focus concepts: `sáu căn`, `sáu trần`, `sáu thức`

## Why This Video

This video is selected because it is a concrete public source with clear
metadata and a focused doctrinal topic.

The topic maps naturally to a small concept set:

- `sáu căn`
- `sáu trần`
- `sáu thức`
- `lục căn, lục trần, lục thức`
- `Kinh Sáu Sáu`

That makes it a good first transcript pilot: small enough to review manually,
but real enough to test source, document, citation, term, and concept modeling.

## Evidence Rules

Evidence can only be added when all four fields are present:

- `source_url`
- timestamp or `locator`
- `evidence_text`
- `review_status`

Transcript Evidence must also include a non-empty `speaker`.

If the source is YouTube, the Evidence must include a non-empty `source_url`.

The initial `review_status` for newly captured transcript Evidence should be
`unreviewed` unless a human has already reviewed the excerpt.

## No Fabricated Transcript Rule

Do not create Evidence nodes from this video until real transcript excerpt text
and timestamps are available.

Placeholder nodes are allowed for:

- `Corpus`
- `Source`
- `Document`
- `Citation`
- `Concept`
- `Term`

Placeholder transcript Evidence is not allowed. A node that looks like Evidence
must contain real excerpt text from the source, not a summary invented during
modeling.

## Review Workflow

1. Obtain the real transcript or manually transcribe a short excerpt.
2. Record the exact timestamp or locator for the excerpt.
3. Preserve the original wording in `evidence_text`.
4. Add `speaker`, `source_url`, and `review_status`.
5. Link the Evidence to `document_transcript_fisp_arohzy8`.
6. Link the Evidence to the relevant concept node.
7. Keep `review_status` as `unreviewed` until a human review is complete.
8. Move to `human_reviewed` or `verified` only after review.

## Expected Output

DKG-003 should produce a reviewable scaffold with:

- one Giác Khang corpus node;
- one YouTube source node;
- one transcript placeholder document node;
- one video-root citation placeholder;
- concept nodes for the Kinh Sáu Sáu pilot;
- Vietnamese and Hán-Việt term nodes;
- provenance relationships from source to document and citation;
- terminology relationships using `DENOTES`;
- no Evidence nodes until real transcript text is available.

## Next Step: Transcript Extraction

The next step is to extract a small number of real transcript excerpts from the
video.

Each excerpt should be added as an Evidence node only after the source URL,
timestamp or locator, exact excerpt text, speaker, and review status are known.

The first extraction batch should stay small so it can be manually reviewed
before larger ingestion work begins.
