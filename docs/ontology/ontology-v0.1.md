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

## Open Questions

- Should passages be modeled as `Text` nodes or as a separate `Passage` type?
- How should variant translations be grouped under one canonical work?
- Should canonical citations be tradition-specific?
- How should confidence and disputed attribution be represented?
