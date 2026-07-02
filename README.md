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

The seed data contract is documented in
`docs/ontology/data-contract-v0.1.md`.

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

## Core Concepts Pilot

The first pilot dataset is in `data/seeds/concepts.json`. Together with the
starter concepts in `data/seeds/core.json`, it contains 30 foundational Dharma
concepts and a small set of relationships between them.

## Text Pilot

The first text-level pilot is in `data/seeds/dhammapada.json`. It adds a
`Text` node for the Dhammapada, citation nodes for selected verses, and concept
links for themes such as mind, heedfulness, ethics, impermanence, and not-self.

The Mahayana text pilot is in `data/seeds/heart_sutra.json`. It adds the Heart
Sutra, selected citation nodes, and links to emptiness, prajnaparamita, the five
aggregates, sense bases, elements, and mantra.

`data/seeds/core.json` also includes a small Mulamadhyamakakarika citation
pilot for Madhyamaka themes such as emptiness, dependent arising, two truths,
and the middle way.

## Terms Pilot

The first language-level pilot is in `data/seeds/terms.json`. It adds Pali and
Sanskrit `Term` nodes for selected concepts and links them back to the concept
layer.

Additional language coverage is in `data/seeds/terms_extended.json`.
The final v0.1 term coverage batch is in `data/seeds/terms_remaining.json`.

## Places & Traditions Pilot

The first place and tradition pilot is in `data/seeds/places_traditions.json`.
It adds historical places, broad tradition nodes, and links between texts,
concepts, schools, and places.

## Validate Seed Data

Run:

```bash
python3 scripts/validate_seed_data.py
```

The validator checks that seed files are valid JSON and that every node has the
required fields: `id`, `type`, and `name`.

You can also run the main project checks with:

```bash
make check
```

The check target includes unit tests for the seed validator.

## Build Graph Explorer

Run:

```bash
python3 scripts/build_graph.py
```

This writes:

- `data/processed/graph.json`
- `docs/artifacts/graph.json`
- `docs/graph-explorer/graph-data.js`

Open `docs/graph-explorer/index.html` in a browser to inspect the graph.

The docs homepage is available at `docs/index.html`.
Deployment notes are in `docs/DEPLOYMENT.md`.

## Write Graph Report

Run:

```bash
python3 scripts/write_graph_report.py
```

This writes `docs/reports/graph-summary.md`, a readable summary of graph size,
node types, relationship types, highly connected nodes, and isolated nodes.

Quality coverage is written to `docs/reports/quality-report.md`.

## Export Neo4j CSV

Run:

```bash
python3 scripts/export_neo4j_csv.py
```

This writes:

- `data/processed/neo4j/nodes.csv`
- `data/processed/neo4j/relationships.csv`
- `docs/artifacts/neo4j/nodes.csv`
- `docs/artifacts/neo4j/relationships.csv`

These CSV files are shaped for Neo4j-style graph imports.

## Export RDF/Turtle

Run:

```bash
python3 scripts/export_rdf_turtle.py
```

This writes `data/processed/rdf/graph.ttl` and
`docs/artifacts/rdf/graph.ttl`, a simple Turtle export for RDF and semantic web
tooling.

## Continuous Checks

GitHub Actions runs `make check` on pushes to `main` and on pull requests. The
workflow also fails if generated graph files or reports are out of date.
