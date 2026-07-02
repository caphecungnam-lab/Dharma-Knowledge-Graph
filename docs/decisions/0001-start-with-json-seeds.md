# Decision 0001: Start With JSON Seed Data

## Status

Accepted

## Context

The project needs a format that is easy to edit, review, and version before
choosing a final graph backend.

## Decision

Start with curated JSON seed files in `data/seeds/`.

Each seed file contains:

- `nodes`: entities such as texts, people, concepts, schools, places, terms,
  and citations
- `relationships`: typed edges between nodes

## Consequences

- Human review stays simple in early versions.
- Git diffs remain readable.
- The same data can later be exported to Neo4j, RDF, or another graph format.
- A lightweight validator is enough for the first stage.
