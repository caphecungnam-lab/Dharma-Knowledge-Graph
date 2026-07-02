# DKG-007: Human Review Workflow

## Purpose

DKG-007 adds a lightweight human review workflow for Evidence nodes created from
YouTube VTT captions.

The first VTT import is useful for bootstrapping the Giac Khang corpus, but it is
not trusted corpus data yet. Caption text can contain timing issues, repeated
phrases, missing Buddhist terminology, or automatic transcription errors.

This workflow keeps imported Evidence unchanged and creates a separate review
queue where a human reviewer can correct text, add notes, and later mark the
Evidence as reviewed or verified.

## Review States

Evidence starts with one of these review states:

- `unreviewed`: Imported from VTT, AI output, or another automated process.
- `human_reviewed`: A human corrected or approved the text.
- `verified`: A human checked the source timestamp, transcript text, and local
  context against the original source.

VTT-derived Evidence must start as `unreviewed`.

## Evidence Quality Criteria

Evidence is suitable for review when it includes:

- `source_url`
- `start_time` and `end_time`, or another precise locator
- `evidence_text`
- `review_status`
- `speaker`
- `document_id`

The reviewer should check that the caption text matches the source audio and that
important Buddhist terms are represented accurately.

## Human Review Rules

Human review must not overwrite the raw imported Evidence file.

The review queue stores:

- `original_evidence_text`: the imported text before review
- `reviewed_evidence_text`: the editable review copy
- `reviewer`: the person who reviewed the Evidence
- `reviewed_at`: the review timestamp
- `review_notes`: notes about corrections or uncertainty
- `review_status`: initially `unreviewed`

The original `evidence_text` field stays unchanged in the queue so reviewers can
compare the imported text with the corrected text.

## Verified Evidence Rules

Evidence should only become `verified` after a human checks:

- the source URL
- the timestamp or locator
- the transcript text
- nearby context in the original teaching

`human_reviewed` means the text was corrected or approved by a human.
`verified` means the Evidence was checked against the original source context.

## File Flow

The DKG-007 file flow is:

1. Raw VTT caption file is stored under `data/raw/`.
2. `scripts/vtt_to_evidence.py` creates
   `data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json`.
3. `scripts/review_evidence.py` copies Evidence nodes into
   `data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json`.
4. A human reviewer edits only the reviewed queue.
5. Later ingestion can promote reviewed or verified Evidence into trusted corpus
   data.

## Next Step

The next step is to add a small reviewed Evidence sample after a human checks the
first VTT-derived segments against the source video.
