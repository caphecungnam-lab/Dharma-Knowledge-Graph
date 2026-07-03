# DKG-017: Corpus Health Gate

## Purpose

DKG-017 adds a read-only health gate for the Giac Khang curated Evidence index.

The gate validates whether the corpus is complete enough for search, local
question answering, citation review, and future CI checks.

## Input

Default input:

```text
data/indexes/giac_khang/curated_evidence_index.json
```

The script reads the index and does not write to corpus data.

## Health Checks

The health gate checks:

- index file availability
- JSON validity
- Evidence node presence
- duplicate Evidence ids
- required Evidence metadata
- citation readiness
- review status
- curated status
- quality score threshold
- ratio thresholds for citation and review gaps

## Error Conditions

These fail by default:

- index file missing
- invalid JSON
- no Evidence nodes
- duplicate Evidence id count above `--max-duplicate-ids`
- missing `evidence_text`
- missing `source_url`
- missing `start_time`
- missing `end_time`
- `quality_score` below `--min-quality`

## Warning Conditions

These warn by default:

- missing `citation_url`
- `review_status` is not `human_reviewed` or `verified`
- `curated_status` is not `curated`
- missing `speaker`
- missing `evidence_type`
- missing `confidence`
- high-quality ratio below threshold
- missing citation ratio above threshold
- unreviewed ratio above threshold

Warnings become failures in strict mode.

## Thresholds

Default thresholds:

```text
--min-quality 50
--min-high-quality-ratio 0
--max-missing-citation-ratio 0.2
--max-unreviewed-ratio 0.2
--max-duplicate-ids 0
```

## CLI Usage

Run the default health gate:

```bash
PYTHONPATH=src python3 scripts/check_corpus_health.py
```

Run strict mode:

```bash
PYTHONPATH=src python3 scripts/check_corpus_health.py --strict
```

Run JSON output:

```bash
PYTHONPATH=src python3 scripts/check_corpus_health.py --json
```

Run through Make:

```bash
make health
make health-strict
```

## CI Integration

The script exits with code `0` when the corpus passes and `1` when it fails.

It is intentionally not part of `make check` yet. It can be added to CI later
once thresholds are stable.

## Safety Rules

- Do not modify raw data.
- Do not modify processed data.
- Do not modify reviewed data.
- Do not modify curated data.
- Validate only the corpus index.
- Preserve Vietnamese Unicode in text and JSON output.

## Next Step

Use the health gate before publishing corpus updates, then decide when to add
strict health checks to CI.
