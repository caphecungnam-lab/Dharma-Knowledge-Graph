# Dharma Knowledge Graph Ontology v0.1

This document defines the first working ontology for the Dharma Knowledge Graph.
It is intentionally small, readable, and suitable for gradual refinement.

## Design Principles

1. Prefer human-readable source data before optimizing for a specific database.
2. Keep every entity stable with a unique `id`.
3. Store provenance early: source, citation, translator, and notes should not be
   treated as afterthoughts.
4. Allow multiple traditions and languages without forcing one canonical view.
5. Model uncertainty explicitly with notes, confidence, or open questions.

## Node Types

### Text

A scripture, commentary, treatise, translation, article, book, or passage.

Required fields:

- `id`
- `type`
- `name`

Suggested fields:

- `alternate_names`
- `language`
- `tradition`
- `date_range`
- `source_url`
- `description`

Examples:

- `text_dhammapada`
- `text_heart_sutra`
- `text_mulamadhyamakakarika`

### Person

An author, translator, teacher, commentator, editor, lineage figure, or scholar.

Suggested fields:

- `alternate_names`
- `birth_year`
- `death_year`
- `tradition`
- `description`

Examples:

- `person_nagarjuna`
- `person_buddhaghosa`
- `person_kumarajiva`

### Concept

A doctrinal, philosophical, contemplative, ethical, or practice concept.

Suggested fields:

- `sanskrit`
- `pali`
- `tibetan`
- `chinese`
- `description`
- `notes`

Examples:

- `concept_dukkha`
- `concept_sunyata`
- `concept_pratityasamutpada`

### School

A Buddhist school, lineage, tradition, or intellectual movement.

Suggested fields:

- `parent_school`
- `region`
- `date_range`
- `description`

Examples:

- `school_theravada`
- `school_madhyamaka`
- `school_yogacara`

### Place

A geographical, historical, monastic, or cultural location.

Suggested fields:

- `country`
- `region`
- `latitude`
- `longitude`
- `description`

Examples:

- `place_bodh_gaya`
- `place_nalanda`

### Term

A lexical form in a specific language or script.

Suggested fields:

- `language`
- `script`
- `transliteration`
- `translation`
- `notes`

Examples:

- `term_dukkha_pali`
- `term_sunyata_sanskrit`

### Citation

A reference to a source location, edition, page, chapter, verse, or URL.

Suggested fields:

- `source`
- `locator`
- `url`
- `accessed_at`
- `notes`

Examples:

- `citation_dhammapada_1_1`
- `citation_mmkv_24_18`

### Corpus

A bounded collection of material selected for ingestion, review, or analysis.

Required fields:

- `id`
- `type`
- `name`

Suggested fields:

- `language`
- `scope`
- `description`
- `notes`

Examples:

- `corpus_giac_khang_pilot`

Purpose in the Evidence-first MVP:

- Defines the boundary of a pilot ingestion set so sources, documents,
  evidence, works, and citations can be reviewed as one collection.

### Source

A provider, edition, repository, notebook, dataset, or other upstream origin
from which documents are derived.

Required fields:

- `id`
- `type`
- `name`

Suggested fields:

- `source_type`
- `language`
- `url`
- `accessed_at`
- `description`
- `notes`

Examples:

- `source_giac_khang_notes`

Purpose in the Evidence-first MVP:

- Records where pilot documents came from before any extraction, enrichment, or
  interpretation happens.

### Document

An ingestible unit derived from a source, such as a note, page, chapter,
article, transcript, file, or extracted passage.

Required fields:

- `id`
- `type`
- `name`

Suggested fields:

- `document_type`
- `language`
- `locator`
- `url`
- `description`
- `notes`

Examples:

- `document_giac_khang_mvp_notes`

Purpose in the Evidence-first MVP:

- Represents the concrete unit that can be reviewed, cited, and used to derive
  evidence nodes.

### Evidence

A claim-supporting excerpt, observation, annotation, or structured assertion
derived from a document.

Required fields:

- `id`
- `type`
- `name`

Suggested fields:

- `evidence_text`
- `evidence_type`
- `confidence`
- `locator`
- `language`
- `notes`

Examples:

- `evidence_giac_khang_sunyata_001`

Purpose in the Evidence-first MVP:

- Provides the inspectable support for concept links so graph claims can be
  traced back to source material.

### Work

An abstract intellectual work that can group documents, translations, editions,
or extracted passages.

Required fields:

- `id`
- `type`
- `name`

Suggested fields:

- `alternate_names`
- `language`
- `tradition`
- `date_range`
- `description`
- `notes`

Examples:

- `work_mulamadhyamakakarika`

Purpose in the Evidence-first MVP:

- Groups documents or citations that represent the same intellectual work
  without forcing every edition or extracted document to become a canonical
  `Text`.

## Relationship Types

### `AUTHORED_BY`

Connects a `Text` to a `Person`.

Example:

- `text_mulamadhyamakakarika` `AUTHORED_BY` `person_nagarjuna`

### `TRANSLATED_BY`

Connects a translated `Text` to a `Person`.

### `COMMENTS_ON`

Connects a commentary, article, or note to the text or concept it explains.

### `MENTIONS`

Connects a text or citation to a concept, person, place, school, or term.

### `DEFINES`

Connects a text, citation, or note to a concept or term it defines.

### `RELATED_TO`

Connects concepts or entities with a broad semantic relationship.

Use this sparingly. Prefer a more specific relationship when possible.

### `BELONGS_TO_SCHOOL`

Connects a person, text, concept framing, or lineage figure to a school.

### `LOCATED_IN`

Connects a place, institution, event, or source tradition to a location.

### `CITES`

Connects a text, note, or claim to a citation.

### `BELONGS_TO_CORPUS`

Connects a source, document, work, citation, text, or evidence node to the
bounded corpus that contains it.

### `DERIVED_FROM`

Records provenance from a derived entity to its upstream source entity.

Examples:

- `document_giac_khang_mvp_notes` `DERIVED_FROM` `source_giac_khang_notes`
- `evidence_giac_khang_sunyata_001` `DERIVED_FROM` `document_giac_khang_mvp_notes`

### `HAS_DOCUMENT`

Connects a corpus, source, or work to an ingestible document.

### `HAS_EVIDENCE`

Connects a document, work, citation, or text to evidence extracted from it.

### `EVIDENCES`

Connects an evidence node to the concept, term, text, or work that it supports.

Example:

- `evidence_giac_khang_sunyata_001` `EVIDENCES` `concept_sunyata`

### `HAS_CITATION`

Connects evidence, documents, works, or texts to a citation node.

## ID Conventions

Use lowercase snake case:

- `text_heart_sutra`
- `person_nagarjuna`
- `concept_sunyata`
- `term_sunyata_sanskrit`
- `citation_heart_sutra_conze_1958`

Prefixes should match node types:

- `text_`
- `person_`
- `concept_`
- `school_`
- `place_`
- `term_`
- `citation_`
- `corpus_`
- `source_`
- `document_`
- `evidence_`
- `work_`

## Open Questions

- Should passages be modeled as `Text`, `Document`, or a separate `Passage`
  type?
- How should variant translations be grouped under one canonical work?
- Should canonical citations be tradition-specific?
- How should confidence and disputed attribution be represented?
