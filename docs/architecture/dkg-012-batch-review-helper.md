# DKG-012: Batch Review Helper

## Purpose

DKG-012 adds a command-line review helper for batch Evidence review.

The first batch contains 50 VTT-derived Evidence nodes. Editing those nodes
directly in JSON is slow and easy to break, so this helper creates a separate
review queue and provides small commands for listing, showing, approving,
editing, rejecting, and counting Evidence review states.

## Input

The default input is the processed batch output from DKG-011:

```text
data/processed/giac_khang/FISpARohzy8/evidence_batch_001.json
```

Processed Evidence is treated as imported source material. It must not be
overwritten by human review.

## Output

The default review output is:

```text
data/reviewed/giac_khang/FISpARohzy8/evidence_batch_001_review_queue.json
```

The review queue is valid JSON and can be passed to the promotion script after
human review.

## Review Fields

Each Evidence node in the review queue includes:

- `original_evidence_text`
- `reviewed_evidence_text`
- `original_review_status`
- `review_status`
- `reviewer`
- `reviewed_at`
- `review_notes`

The original imported `evidence_text` is preserved. Human-corrected text is
stored separately in `reviewed_evidence_text`.

## CLI Workflow

Create the review queue:

```bash
python3 scripts/batch_review_helper.py init \
  --input data/processed/giac_khang/FISpARohzy8/evidence_batch_001.json \
  --output data/reviewed/giac_khang/FISpARohzy8/evidence_batch_001_review_queue.json
```

List review status:

```bash
python3 scripts/batch_review_helper.py list \
  --path data/reviewed/giac_khang/FISpARohzy8/evidence_batch_001_review_queue.json
```

Show one Evidence node:

```bash
python3 scripts/batch_review_helper.py show evidence_fisp_arohzy8_0007 \
  --path data/reviewed/giac_khang/FISpARohzy8/evidence_batch_001_review_queue.json
```

Approve an Evidence node without text changes:

```bash
python3 scripts/batch_review_helper.py approve evidence_fisp_arohzy8_0007 \
  --path data/reviewed/giac_khang/FISpARohzy8/evidence_batch_001_review_queue.json \
  --reviewer Minh
```

Edit and approve an Evidence node:

```bash
python3 scripts/batch_review_helper.py edit evidence_fisp_arohzy8_0007 \
  --path data/reviewed/giac_khang/FISpARohzy8/evidence_batch_001_review_queue.json \
  --text "Corrected reviewed text here." \
  --reviewer Minh \
  --notes "Corrected punctuation and Buddhist proper nouns."
```

Reject an Evidence node:

```bash
python3 scripts/batch_review_helper.py reject evidence_fisp_arohzy8_0007 \
  --path data/reviewed/giac_khang/FISpARohzy8/evidence_batch_001_review_queue.json \
  --reviewer Minh \
  --notes "Caption is too broken to use."
```

Show review counts:

```bash
python3 scripts/batch_review_helper.py stats \
  --path data/reviewed/giac_khang/FISpARohzy8/evidence_batch_001_review_queue.json
```

Promote reviewed Evidence after human review:

```bash
python3 scripts/promote_reviewed_evidence.py \
  --input data/reviewed/giac_khang/FISpARohzy8/evidence_batch_001_review_queue.json \
  --output data/curated/giac_khang/FISpARohzy8/evidence_batch_001_curated.json
```

## Safety Rules

- Do not overwrite processed Evidence.
- Preserve `original_evidence_text`.
- Store human-corrected text in `reviewed_evidence_text`.
- Do not duplicate `review_status` keys.
- Use `rejected` for Evidence that should not be promoted.
- Keep output JSON formatted with 2-space indentation.

## Promotion Compatibility

Only Evidence with:

```text
review_status: human_reviewed
```

is eligible for promotion.

Evidence with:

```text
review_status: rejected
```

must be skipped by promotion.

## Next Step

Use the helper to review `evidence_batch_001_review_queue.json`, then promote
the reviewed subset into curated batch output.
