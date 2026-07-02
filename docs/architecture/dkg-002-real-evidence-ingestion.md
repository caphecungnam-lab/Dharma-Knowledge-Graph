# DKG-002: Real Evidence Ingestion

This note hardens the Evidence schema so the Dharma Knowledge Graph can ingest
real transcript excerpts from Giac Khang teachings.

## Scope

This task is schema and data-model work only.

In scope:

- Required Evidence fields for real transcript excerpts.
- Allowed values for Evidence classification and review state.
- Seed-data validation rules.
- One unreviewed placeholder sample that follows the real structure.

Out of scope:

- API endpoints.
- Frontend changes.
- Embeddings.
- LLM extraction.
- Automated transcript ingestion.

## Real Evidence Shape

Real Evidence nodes should include:

| Field | Purpose |
| --- | --- |
| `id` | Stable Evidence node ID using the `evidence_` prefix. |
| `type` | Must be `Evidence`. |
| `name` | Short human-readable label. |
| `evidence_text` | Transcript excerpt, citation excerpt, paraphrase, summary, or note. |
| `evidence_type` | Controlled type of evidence. |
| `language` | Language of the evidence text. |
| `confidence` | Current confidence level. |
| `source_kind` | Source medium, such as `youtube`, `local_notes`, or `book`. |
| `source_url` | URL for web sources. Required when `source_kind` is `youtube`. |
| `document_id` | ID of the document represented by this excerpt. |
| `locator` | Human-readable locator such as timestamp, page, or section. |
| `start_time` | Start timestamp for audio/video transcript evidence. |
| `end_time` | End timestamp for audio/video transcript evidence. |
| `speaker` | Speaker name. Required for transcript excerpts. |
| `review_status` | Review lifecycle state. |
| `notes` | Cautions, open questions, or review notes. |

## Allowed Values

Allowed `evidence_type` values:

- `transcript_excerpt`
- `citation_excerpt`
- `paraphrase`
- `ai_summary`
- `human_note`

Allowed `confidence` values:

- `low`
- `medium`
- `high`

Allowed `review_status` values:

- `unreviewed`
- `ai_processed`
- `human_reviewed`
- `verified`

## Validation Rules

The seed validator enforces:

- Evidence nodes must include `evidence_text`.
- Evidence nodes must include `evidence_type`.
- Evidence nodes must include `confidence`.
- Evidence nodes must include `review_status`.
- Evidence nodes with `evidence_type: transcript_excerpt` must include
  `speaker`.
- Evidence nodes with `source_kind: youtube` must include `source_url`.

## Review Meaning

`unreviewed` means the node is structurally valid but should not be treated as a
verified knowledge claim. It can be used to test ingestion, reports, and graph
plumbing while keeping human review explicit.
