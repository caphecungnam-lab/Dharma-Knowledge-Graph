# DKG-009: Citation-Aware Search

## Purpose

DKG-009 adds a lightweight CLI search tool for curated Evidence.

The goal is to find human-reviewed, curated transcript excerpts while preserving
the citation context needed for later verification and graph navigation.

## Input

The default input file is:

`data/curated/giac_khang/FISpARohzy8/evidence_curated.json`

The input can be overridden with:

`--path path/to/evidence_curated.json`

## Search Fields

Search is case-insensitive and preserves Vietnamese Unicode.

The searchable fields are:

- `evidence_text`
- `reviewed_evidence_text`
- `original_evidence_text`
- `notes`
- `review_notes`

Only `Evidence` nodes are returned.

## CLI Usage

Basic usage:

```bash
python3 scripts/search_curated_evidence.py "Kinh Sáu Sáu"
```

Limit results:

```bash
python3 scripts/search_curated_evidence.py "Kinh Sáu Sáu" --limit 3
```

JSON output:

```bash
python3 scripts/search_curated_evidence.py "Kinh Sáu Sáu" --json
```

Custom path:

```bash
python3 scripts/search_curated_evidence.py "Kinh Sáu Sáu" --path data/curated/giac_khang/FISpARohzy8/evidence_curated.json
```

## Result Fields

Each result includes:

- `id`
- `start_time`
- `end_time`
- `speaker`
- `review_status`
- `curated_status`
- `evidence_text`
- `source_url`
- `citation`

The citation string combines speaker, timestamp range, and source URL.

## What This Does Not Do Yet

This is not semantic search.

DKG-009 does not add embeddings, LLM processing, API endpoints, or frontend UI.
It is a deterministic text search over curated Evidence JSON.

## Next Step

The next step is to add verified Evidence and a richer citation object after
timestamp, text, and source context are checked against the original video.
