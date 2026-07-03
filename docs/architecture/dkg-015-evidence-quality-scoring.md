# DKG-015: Evidence Quality Scoring

## Purpose

DKG-015 adds a helper quality score to curated Evidence nodes.

The score helps search and local ask prioritize Evidence that has stronger
metadata, citation support, and human review status.

## Quality Score Meaning

`quality_score` is a practical retrieval signal from `0` to `100`.

It is not a doctrinal truth score. It does not decide whether an interpretation
is correct. It only indicates whether the Evidence node is complete enough to be
useful for review, search, and grounded answers.

## Quality Flags

`quality_flags` records which scoring conditions were met:

- `has_text`
- `has_start_time`
- `has_end_time`
- `has_source_url`
- `has_citation_url`
- `human_reviewed`
- `verified`
- `curated`
- `has_speaker`
- `has_evidence_type`
- `has_confidence`

## Scoring Rules

Start at `0`.

Add:

- `+20` if `evidence_text` exists and has at least 20 characters
- `+10` if `start_time` exists
- `+10` if `end_time` exists
- `+10` if `source_url` exists
- `+10` if `citation_url` exists or can be generated from `source_url + start_time`
- `+15` if `review_status == "human_reviewed"`
- `+20` if `review_status == "verified"`
- `+10` if `curated_status == "curated"`
- `+5` if `speaker` exists
- `+5` if `evidence_type` exists
- `+5` if `confidence` exists

The score is capped at `100`.

## Search Ranking

Search ranks matched Evidence by:

1. Keyword and alias match score
2. `quality_score` descending
3. `start_time` ascending

Search output includes the quality score and quality flags.

## Ask Ranking

Ask retrieves matched Evidence from the curated index and prefers higher-quality
matches when keyword match strength is equal.

The answer remains grounded only in matched Evidence text.

## Safety Rules

- Do not change raw data.
- Do not change processed data.
- Do not change reviewed data.
- Do not alter `evidence_text`.
- Add scoring only when building the curated index.
- Do not mark Evidence as verified unless the Evidence already says it is
  verified.

## Limitations

Quality scoring rewards metadata completeness and review status. It does not
measure doctrinal accuracy, translation quality, or philosophical importance.

Human review remains the authority for corpus trust.

## Next Step

Use quality scores to guide review priorities and improve the ranking of
search/ask results as the curated corpus grows.
