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
Search also normalizes whitespace and can match without Vietnamese diacritics.

The searchable fields are:

- `evidence_text`
- `reviewed_evidence_text`
- `original_evidence_text`
- `notes`
- `review_notes`
- `name`

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

Debug query expansion:

```bash
python3 scripts/search_curated_evidence.py "Kinh Sáu Sáu" --debug
```

## Query Aliases

The search tool expands common Vietnamese and romanized query forms:

- `kinh sáu sáu` also searches `kinh 66`, `kinh sáu sáu`, and `bài kinh 66`.
- `sáu sáu` also searches `66` and `sáu sáu`.
- `luc can` also searches `lục căn` and `sáu căn`.
- `luc tran` also searches `lục trần` and `sáu trần`.
- `luc thuc` also searches `lục thức` and `sáu thức`.

The tool also compares normalized text without Vietnamese diacritics, so
unaccented queries can match accented Evidence text.

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

## Debug Output

With `--debug`, text output includes:

- curated file path
- number of Evidence nodes loaded
- normalized query terms
- fields searched

With `--debug --json`, the output contains a `debug` object and a `results`
array.

## What This Does Not Do Yet

This is not semantic search.

DKG-009 does not add embeddings, LLM processing, API endpoints, or frontend UI.
It is a deterministic text search over curated Evidence JSON.

## Next Step

The next step is to add verified Evidence and a richer citation object after
timestamp, text, and source context are checked against the original video.
