# DKG-008: Promote Reviewed Evidence

## Purpose

This step promotes `human_reviewed` Evidence from the review queue into curated
corpus data.

Reviewed Evidence is still not verified. It has passed a human text review, but
the source timestamp, source context, and final citation quality still need a
separate verification step.

## Input

The input file is:

`data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json`

Only nodes with:

`review_status: "human_reviewed"`

are eligible for promotion.

## Output

The output file is:

`data/curated/giac_khang/FISpARohzy8/evidence_curated.json`

The curated file contains promoted Evidence nodes and their Evidence-to-source
relationships.

## Promotion Rules

Promotion follows these rules:

- Promote only Evidence nodes with `review_status: "human_reviewed"`.
- Do not promote `unreviewed` Evidence.
- Preserve `original_evidence_text`.
- Use `reviewed_evidence_text` as curated `evidence_text`.
- Preserve `reviewed_evidence_text` for traceability.
- Keep timestamps, `source_url`, `document_id`, `speaker`, `source_kind`,
  `language`, `evidence_type`, `confidence`, and citation links.
- Preserve `review_notes`.
- Add `curated_status: "curated"`.
- Add `curated_at: "2026-07-03"`.
- Add `curator: "Minh"`.
- Do not set `review_status` to `verified`.
- Do not overwrite reviewed data.
- Do not change raw or processed Evidence data.

## Curated Evidence Fields

Curated Evidence keeps the Evidence shape needed by the graph:

- `id`
- `type`
- `name`
- `evidence_text`
- `evidence_type`
- `language`
- `confidence`
- `source_kind`
- `source_url`
- `document_id`
- `start_time`
- `end_time`
- `speaker`
- `review_status`
- `original_review_status`
- `original_evidence_text`
- `reviewed_evidence_text`
- `review_notes`
- `curated_status`
- `curated_at`
- `curator`

## What Is Not Verified Yet

Curated Evidence is not verified Evidence.

Verification still requires checking:

- source timestamp
- transcript text
- surrounding source context
- citation target
- Buddhist terminology

## File Flow

The promotion flow is:

1. VTT-derived Evidence remains in
   `data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json`.
2. Human review happens in
   `data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json`.
3. Only `human_reviewed` Evidence is promoted into
   `data/curated/giac_khang/FISpARohzy8/evidence_curated.json`.
4. Raw processed Evidence and reviewed queue data are preserved for traceability.

## Next Step

The next step is to create a verification workflow that can promote curated
Evidence into verified Evidence after timestamp, text, and source context are
checked against the original video.
