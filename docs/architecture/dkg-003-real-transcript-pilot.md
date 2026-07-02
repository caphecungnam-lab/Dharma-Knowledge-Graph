# DKG-003: Real Transcript Pilot

This note defines the first real-source transcript scaffold for the Giac Khang
Corpus. It creates source, document, citation, concept, and term structure for a
specific YouTube teaching without inventing transcript evidence.

## Purpose

DKG-003 prepares the graph to receive real transcript excerpts from a known
teaching source. The goal is to model provenance and target concepts before any
Evidence nodes are added.

## Source Metadata

- YouTube URL: `https://www.youtube.com/watch?v=FISpARohzy8`
- YouTube video ID: `FISpARohzy8`
- Title: `1A. KINH 6 6 L2CÂU 1 P1`
- Speaker: `HT. Thích Giác Khang`
- Channel: `PHÁP ÂM SƯ KHANG`
- Topic: `Kinh Sáu Sáu`
- Focus concepts: `sáu căn`, `sáu trần`, `sáu thức`

## Why This Video

This video is selected as the first real transcript pilot because it has a
stable public source URL, a clear speaker, a clear channel, and a focused topic
that maps naturally to a small set of concepts and Vietnamese/Hán-Việt terms.

## Evidence Rules

Evidence can only be added when all four fields are present:

- `source_url`
- timestamp or `locator`
- `evidence_text`
- `review_status`

Transcript Evidence must also include `speaker`.

## No Fabricated Transcript Rule

Do not create Evidence nodes from this video until real transcript excerpt text
and timestamps are available. Placeholder nodes are allowed for `Source`,
`Document`, and `Citation`, but not for transcript Evidence.

## Review Workflow

1. Import or manually capture a real transcript excerpt.
2. Record the exact timestamp or locator.
3. Add the excerpt as `evidence_text`.
4. Set `review_status` to `unreviewed`.
5. Link the Evidence to the transcript document and relevant concept.
6. Move to `human_reviewed` or `verified` only after review.

## Expected Output

DKG-003 should produce:

- one Giac Khang corpus node;
- one YouTube source node;
- one transcript placeholder document node;
- one video-root citation placeholder;
- concept and term nodes for the Kinh Sáu Sáu pilot;
- provenance and terminology relationships;
- no Evidence nodes until real transcript text is available.

## Next Step: Transcript Extraction

The next step is to obtain a real transcript for the video and extract a small
reviewable set of timestamped excerpts. Each excerpt should become an Evidence
node only after the source URL, timestamp or locator, excerpt text, speaker, and
review status are known.
