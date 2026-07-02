# DKG-005: VTT to First Evidence

DKG-005 converts the first real Vietnamese YouTube VTT caption segments for
`FISpARohzy8` into a small Evidence first pass.

## Purpose

The purpose is to test a real caption-to-Evidence path without inventing,
paraphrasing, or summarizing transcript text.

The first pass is intentionally limited to five caption segments so that the
output can be reviewed manually before larger transcript ingestion.

## Input

Input file:

```text
data/raw/giac_khang/FISpARohzy8/source.vi.vtt
```

The VTT file is treated as the source of truth for transcript text in this
step.

## Parsing Rule

The parser:

- ignores `WEBVTT` headers and metadata lines;
- reads VTT timestamp ranges;
- removes HTML and inline timing tags;
- collapses whitespace;
- keeps Vietnamese Unicode text;
- skips empty captions;
- uses only the first five valid caption segments.

## Evidence Output

The output is written to:

```text
data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json
```

Each Evidence node includes source URL, document ID, start and end time,
speaker, review status, and the exact cleaned VTT caption text.

The output also includes relationships from each Evidence node to:

- `citation_youtube_fisp_arohzy8` using `HAS_CITATION`;
- `document_transcript_fisp_arohzy8` using `DERIVED_FROM`.

## Review Status

All generated Evidence nodes use:

```text
review_status: unreviewed
confidence: low
```

This marks the output as structurally useful but not yet human verified.

## No Fabricated Transcript Rule

Do not invent transcript text.

Do not paraphrase.

Do not summarize.

Only text found in the VTT file may appear in `evidence_text`.

## Next Step

Review the five generated Evidence nodes manually for caption accuracy and
Buddhist terminology before promoting them into seed data.
