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
- `Person`
- `Place`
- `School`
- `Term`
- `Text`

Node IDs must use lowercase snake case and match the type prefix:

| Type | Prefix |
| --- | --- |
| Citation | `citation_` |
| Concept | `concept_` |
| Person | `person_` |
| Place | `place_` |
| School | `school_` |
| Term | `term_` |
| Text | `text_` |

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
| `CITES` | `Citation`, `Text` | `Citation` |
| `COMMENTS_ON` | `Citation`, `Text` | `Concept`, `Text` |
| `DEFINES` | `Citation`, `Concept`, `Term`, `Text` | `Concept`, `Term` |
| `LOCATED_IN` | `Person`, `Place`, `School`, `Text` | `Place` |
| `MENTIONS` | `Citation`, `Concept`, `Text` | `Concept`, `Person`, `Place`, `School`, `Term` |
| `RELATED_TO` | any known node type | any known node type |
| `TRANSLATED_BY` | `Text` | `Person` |

## Validation

Run:

```bash
make check
```

This validates seed data, rebuilds graph artifacts, exports Neo4j CSV and
RDF/Turtle, and checks Python syntax.
