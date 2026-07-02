# DKG-008: Graph Data Scope

## Purpose

DKG-008 scopes Graph Explorer to the Giác Khang Corpus by default.

The repository still keeps older seed data for ontology development and examples,
but the default user-facing graph should not mix English demo material with the
Vietnamese Giác Khang transcript pilot.

## Data Loading Modes

Graph Explorer supports three data loading modes:

- `giac_khang`: default mode for the Giác Khang Corpus pilot.
- `seeds_only`: all files under `data/seeds/`.
- `all_data`: all seed files plus processed, reviewed, and curated Giác Khang
  Evidence outputs.

The visible UI labels are:

- Giác Khang
- Seeds
- All

## Default Giác Khang Scope

The default `giac_khang` mode loads:

- `data/seeds/giac_khang_kinh_sau_sau_fisp_arohzy8.json`
- `data/processed/giac_khang/FISpARohzy8/evidence_first_pass.json`
- `data/reviewed/giac_khang/FISpARohzy8/evidence_review_queue.json`, when present
- `data/curated/giac_khang/FISpARohzy8/evidence_curated.json`, when present

This keeps the default graph focused on the first real Giác Khang video source
and its Evidence workflow.

## Excluded From Default Scope

The default `giac_khang` mode does not load the older demo and ontology seed
files:

- `data/seeds/giac_khang_pilot.json`
- `data/seeds/heart_sutra.json`
- `data/seeds/dhammapada.json`
- `data/seeds/concepts.json`
- `data/seeds/terms.json`
- `data/seeds/terms_extended.json`
- `data/seeds/terms_remaining.json`
- `data/seeds/places_traditions.json`

These files remain available through `seeds_only` and `all_data`.

## Language Filter

Graph Explorer includes a language filter with:

- All
- vi
- en
- pali
- sanskrit

The filter normalizes common language labels such as `Vietnamese`, `English`,
`Pali`, and `Sanskrit` to their lowercase mode values.

## Source Badges

Nodes include a `source_badge` field for visual review:

- `corpus`
- `seed`
- `processed`
- `reviewed`
- `curated`

When duplicate Evidence IDs exist across processed, reviewed, and curated
outputs, later workflow stages override earlier stages in the scoped graph. This
lets reviewed or curated Evidence appear as the current review surface without
rewriting the raw imported file.

## Next Step

The next step is to promote human-reviewed Evidence into a curated Evidence file
after timestamp, text, and source context have been checked.
