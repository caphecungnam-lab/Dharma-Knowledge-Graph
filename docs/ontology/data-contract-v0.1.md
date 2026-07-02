# Data Contract v0.1

This document defines the minimum contract for seed files in `data/seeds/`.

## Seed File Shape

Each seed file must be valid JSON with two top-level arrays:

```json
{
  "nodes": [],
  "relationships": []
}
```

## Nodes

Every node must include:

- `id`
- `type`
- `name`

Allowed node types:

- `Citation`
- `Concept`
- `Corpus`
- `Document`
- `Evidence`
- `Person`
- `Place`
- `School`
- `Source`
- `Term`
- `Text`
- `Work`

Node IDs must use lowercase snake case and match the type prefix:

| Type | Prefix |
| --- | --- |
| Citation | `citation_` |
| Concept | `concept_` |
| Corpus | `corpus_` |
| Document | `document_` |
| Evidence | `evidence_` |
| Person | `person_` |
| Place | `place_` |
| School | `school_` |
| Source | `source_` |
| Term | `term_` |
| Text | `text_` |
| Work | `work_` |

## Relationships

Every relationship must include:

- `source`
- `type`
- `target`

Relationship IDs are implicit: the combination of `source`, `type`, and
`target` must be unique across all seed files.

Allowed relationship types and type pairs:

| Relationship | Source Types | Target Types |
| --- | --- | --- |
| `AUTHORED_BY` | `Text` | `Person` |
| `BELONGS_TO_SCHOOL` | `Concept`, `Person`, `School`, `Text` | `School` |
| `BELONGS_TO_CORPUS` | `Citation`, `Document`, `Evidence`, `Source`, `Work` | `Corpus` |
| `CITES` | `Citation`, `Text` | `Citation` |
| `COMMENTS_ON` | `Citation`, `Text` | `Concept`, `Text` |
| `DEFINES` | `Citation`, `Concept`, `Term`, `Text` | `Concept`, `Term` |
| `DENOTES` | `Term` | `Concept` |
| `DERIVED_FROM` | `Citation`, `Document`, `Evidence`, `Work` | `Citation`, `Document`, `Source`, `Work` |
| `EVIDENCES` | `Evidence` | `Concept`, `Term`, `Text`, `Work` |
| `HAS_CITATION` | `Document`, `Evidence`, `Text`, `Work` | `Citation` |
| `HAS_DOCUMENT` | `Corpus`, `Source`, `Work` | `Document` |
| `HAS_EVIDENCE` | `Citation`, `Document`, `Work` | `Evidence` |
| `LOCATED_IN` | `Person`, `Place`, `School`, `Text` | `Place` |
| `MENTIONS` | `Citation`, `Concept`, `Document`, `Evidence`, `Text`, `Work` | `Concept`, `Person`, `Place`, `School`, `Term`, `Text`, `Work` |
| `RELATED_TO` | any known node type | any known node type |
| `TRANSLATED_BY` | `Text` | `Person` |

## Evidence-First MVP Nodes

The 21-day MVP adds provenance-oriented node types while keeping existing
ontology work intact:

- `Corpus`: a bounded collection selected for ingestion.
- `Source`: an upstream provider, edition, dataset, notebook, or repository.
- `Document`: an ingestible unit derived from a source.
- `Evidence`: an excerpt, annotation, or structured assertion derived from a
  document.
- `Work`: an abstract intellectual work grouping documents, editions,
  translations, or extracted passages.

Evidence-first pilot data should preserve this trace:

```text
Corpus -> Source -> Document -> Evidence -> Concept
```

When a locator is available, evidence should also connect to a `Citation` via
`HAS_CITATION`.

## Real Evidence Fields

DKG-002 prepares Evidence nodes for real transcript excerpts from Giac Khang
teachings. Real Evidence nodes should include:

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
- `locator`
- `start_time`
- `end_time`
- `speaker`
- `review_status`
- `notes`

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

Validation currently enforces these Evidence fields:

- `evidence_text`
- `evidence_type`
- `confidence`
- `review_status`

Conditional validation:

- If `evidence_type` is `transcript_excerpt`, `speaker` is required.
- If `source_kind` is `youtube`, `source_url` is required.

Evidence can only be added when all four fields are present:

- `source_url`
- timestamp or `locator`
- `evidence_text`
- `review_status`

## Validation

Run:

```bash
make check
```

This validates seed data, rebuilds graph artifacts, exports Neo4j CSV and
RDF/Turtle, and checks Python syntax.
