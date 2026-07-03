# DKG-013: Batch Curated Promotion and Search Merge

## Purpose

DKG-013 allows the Giac Khang corpus to grow beyond one curated Evidence file.
It promotes reviewed batch Evidence into curated data, then merges all curated
Evidence into one searchable corpus index.

The result is a local curated corpus that search and ask tools can query as a
whole.

## Input Files

The batch review input is:

```text
data/reviewed/giac_khang/FISpARohzy8/evidence_batch_001_review_queue.json
```

Existing curated files are read from:

```text
data/curated/giac_khang/
```

The index builder recursively includes:

- `*_curated.json`
- `evidence_curated.json`

## Output Files

The curated batch output is:

```text
data/curated/giac_khang/FISpARohzy8/evidence_batch_001_curated.json
```

The merged corpus index is:

```text
data/indexes/giac_khang/curated_evidence_index.json
```

## Promotion Rule

Only Evidence nodes with:

```text
review_status: human_reviewed
```

are promoted.

Evidence nodes with `review_status: rejected` or `review_status: unreviewed`
are skipped.

During promotion:

- `original_evidence_text` is preserved.
- `reviewed_evidence_text` becomes `evidence_text`.
- `source_url`, `speaker`, `start_time`, `end_time`, `language`,
  `source_kind`, `evidence_type`, `confidence`, and `document_id` are preserved.
- `curated_status` is set to `curated`.
- `curated_at` is an ISO local datetime unless already present.
- `curator` is the reviewer when available, otherwise `Minh`.
- Evidence is not marked as verified.

## Merge Rule

The curated index is built by recursively reading curated JSON files from the
Giac Khang curated directory.

The index output has this shape:

```json
{
  "metadata": {},
  "nodes": [],
  "relationships": []
}
```

Metadata includes:

- `index_name`
- `corpus_id`
- `generated_at`
- `evidence_count`
- `source_files`

## Deduplication Rule

Evidence is deduplicated by `id`.

If the same Evidence id appears in multiple files, the merge prefers the newest
item with:

```text
curated_status: curated
```

Output ordering is deterministic:

1. `document_id` or `source_id`
2. `start_time`
3. Evidence `id`

## Search Scope

`scripts/search_curated_evidence.py` now defaults to:

```text
data/indexes/giac_khang/curated_evidence_index.json
```

It still supports `--path` for custom files and keeps Vietnamese-friendly alias
matching.

## Ask Scope

`scripts/ask_curated_evidence.py` also defaults to the merged curated index.

Answers are constructed only from matched curated Evidence. Each answer keeps
Evidence citation metadata, including video/source identity, timestamp, and
source URL.

## Safety Rules

- Do not overwrite reviewed files.
- Do not overwrite raw files.
- Do not overwrite processed files.
- Promote only human-reviewed Evidence.
- Skip rejected and unreviewed Evidence.
- Preserve original Evidence text for traceability.
- Do not mark Evidence as verified.
- Keep index output deterministic and valid JSON.

## Next Step

Use the batch review helper to review more Evidence nodes, promote the reviewed
subset, then rebuild the curated index before searching or asking questions.
