# DKG-016: Corpus Dashboard

## Purpose

DKG-016 adds a read-only corpus dashboard for the Giac Khang curated Evidence
corpus.

The dashboard summarizes corpus size, review progress, citation readiness,
quality distribution, missing metadata, and source coverage.

## Input

The default input is:

```text
data/indexes/giac_khang/curated_evidence_index.json
```

The dashboard reads only the curated Evidence index.

## Outputs

The default outputs are:

```text
reports/giac_khang/corpus_dashboard.md
reports/giac_khang/corpus_dashboard.json
```

The Markdown report is for human review. The JSON report is for automation and
future dashboard integrations.

## Metrics

The dashboard reports:

- total Evidence
- curated Evidence count
- human-reviewed count
- verified count
- rejected count
- unreviewed count
- citation URL availability
- average, minimum, and maximum quality score
- missing metadata counts

## Quality Buckets

Quality is grouped into three buckets:

- high quality: `quality_score >= 80`
- medium quality: `50 <= quality_score < 80`
- needs review: `quality_score < 50`

The thresholds can be changed with CLI options.

## Missing Metadata Checks

The dashboard checks missing values for:

- `evidence_text`
- `start_time`
- `end_time`
- `source_url`
- `citation_url`
- `speaker`
- `evidence_type`
- `confidence`

These checks help identify Evidence that should be improved before broader use.

## Source Coverage

Source coverage summarizes Evidence by:

- `source_url`
- `document_id`
- `speaker`

It also reports the earliest start time and latest end time found in the index.

## CLI Usage

Build the dashboard with defaults:

```bash
python3 scripts/build_corpus_dashboard.py
```

Or through Make:

```bash
make dashboard
```

Custom input and output paths:

```bash
python3 scripts/build_corpus_dashboard.py \
  --input data/indexes/giac_khang/curated_evidence_index.json \
  --output-md reports/giac_khang/corpus_dashboard.md \
  --output-json reports/giac_khang/corpus_dashboard.json
```

Custom thresholds:

```bash
python3 scripts/build_corpus_dashboard.py \
  --min-high-quality 85 \
  --min-needs-review 60
```

## Safety Rules

- Do not change raw data.
- Do not change processed data.
- Do not change reviewed data.
- Do not change curated data.
- Treat dashboard generation as read-only reporting.
- Preserve Vietnamese Unicode in reports.

## Next Step

Use the dashboard to decide whether to review more Evidence, rebuild citation
links, continue batch ingestion, or expand source coverage.
