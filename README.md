# Dharma Knowledge Graph

This repository collects source material, structured data, and tooling for a
Dharma knowledge graph.

The first goal is to model Dharma texts, concepts, people, places, traditions,
terms, and citations in a format that is easy to review by humans and can later
be loaded into a graph database or semantic web stack.

## Project Shape

- `data/raw/`: original source files and exports
- `data/seeds/`: small curated JSON data used to bootstrap the graph
- `data/processed/`: generated or normalized graph-ready data
- `docs/ontology/`: entity and relationship design notes
- `docs/decisions/`: architecture and modeling decisions
- `notebooks/`: exploratory analysis
- `scripts/`: utility scripts for validation and data processing
- `src/dharma_kg/`: project source code
- `tests/`: checks for scripts and data contracts

## Current Direction

The project starts with simple JSON seed files and a lightweight ontology.
This keeps early editing easy while leaving room to export later to:

- Neo4j for graph database exploration
- RDF/OWL for semantic web interoperability
- Markdown or static site views for human-readable study notes

## First Data Model

The initial ontology is documented in
`docs/ontology/ontology-v0.1.md`.

Core node types:

- `Text`
- `Person`
- `Concept`
- `School`
- `Place`
- `Term`
- `Citation`

Core relationship types:

- `AUTHORED_BY`
- `TRANSLATED_BY`
- `COMMENTS_ON`
- `MENTIONS`
- `DEFINES`
- `RELATED_TO`
- `BELONGS_TO_SCHOOL`
- `LOCATED_IN`
- `CITES`

## Validate Seed Data

Run:

```bash
python3 scripts/validate_seed_data.py
```

The validator checks that seed files are valid JSON and that every node has the
required fields: `id`, `type`, and `name`.
