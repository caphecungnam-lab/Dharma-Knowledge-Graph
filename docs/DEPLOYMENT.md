# Deployment

This project is designed to publish the `docs/` folder with GitHub Pages.

## GitHub Pages Settings

Use these repository settings:

- Source: `Deploy from a branch`
- Branch: `main`
- Folder: `/docs`

After GitHub Pages finishes deploying, the site should be available at:

```text
https://caphecungnam-lab.github.io/Dharma-Knowledge-Graph/
```

## Public Site Entry Points

- Homepage: `docs/index.html`
- Graph Explorer: `docs/graph-explorer/index.html`
- Graph JSON: `docs/artifacts/graph.json`
- Neo4j CSV: `docs/artifacts/neo4j/`
- RDF/Turtle: `docs/artifacts/rdf/graph.ttl`
- Reports: `docs/reports/`

## Local Checks

Run:

```bash
make check
```

This validates seed data, rebuilds public docs artifacts, checks docs links,
runs tests, and compiles Python scripts.
