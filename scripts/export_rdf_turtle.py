#!/usr/bin/env python3
"""Export processed graph data to a simple RDF/Turtle file."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = ROOT / "data" / "processed" / "graph.json"
RDF_DIR = ROOT / "data" / "processed" / "rdf"
TTL_PATH = RDF_DIR / "graph.ttl"
DOCS_RDF_DIR = ROOT / "docs" / "artifacts" / "rdf"
DOCS_TTL_PATH = DOCS_RDF_DIR / "graph.ttl"

BASE_IRI = "https://caphecungnam-lab.github.io/Dharma-Knowledge-Graph/"
ENTITY_PREFIX = "dkge"
ONTOLOGY_PREFIX = "dkg"


PROPERTY_MAP = {
    "AUTHORED_BY": "authoredBy",
    "BELONGS_TO_CORPUS": "belongsToCorpus",
    "BELONGS_TO_SCHOOL": "belongsToSchool",
    "CITES": "cites",
    "COMMENTS_ON": "commentsOn",
    "DEFINES": "defines",
    "DENOTES": "denotes",
    "DERIVED_FROM": "derivedFrom",
    "EVIDENCES": "evidences",
    "HAS_CITATION": "hasCitation",
    "HAS_DOCUMENT": "hasDocument",
    "HAS_EVIDENCE": "hasEvidence",
    "LOCATED_IN": "locatedIn",
    "MENTIONS": "mentions",
    "RELATED_TO": "relatedTo",
    "TRANSLATED_BY": "translatedBy",
}

LITERAL_FIELDS = [
    "name",
    "description",
    "category",
    "pali",
    "sanskrit",
    "tibetan",
    "chinese",
    "tradition",
    "language",
    "script",
    "transliteration",
    "translation",
    "country",
    "region",
    "source",
    "locator",
    "source_kind",
    "source_url",
    "channel",
    "title",
    "topic",
    "document_id",
    "document_kind",
    "start_time",
    "end_time",
    "speaker",
    "review_status",
    "url",
    "accessed_at",
    "notes",
    "scope",
    "source_type",
    "document_type",
    "evidence_type",
    "evidence_text",
    "confidence",
    "source_file",
]


def load_graph() -> dict:
    if not GRAPH_PATH.exists():
        raise FileNotFoundError(
            f"{GRAPH_PATH.relative_to(ROOT)} does not exist. "
            "Run scripts/build_graph.py first."
        )
    return json.loads(GRAPH_PATH.read_text(encoding="utf-8"))


def camel_case(value: str) -> str:
    parts = re.split(r"[_\s-]+", value.strip())
    if not parts:
        return value
    first, *rest = parts
    return first.lower() + "".join(part.capitalize() for part in rest)


def ttl_string(value: object) -> str:
    text = str(value)
    escaped = (
        text.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
    )
    return f'"{escaped}"'


def entity_ref(entity_id: str) -> str:
    return f"{ENTITY_PREFIX}:{entity_id}"


def ontology_ref(name: str) -> str:
    return f"{ONTOLOGY_PREFIX}:{name}"


def predicate_ref(field: str) -> str:
    return ontology_ref(camel_case(field))


def relationship_predicate(relationship_type: str) -> str:
    return ontology_ref(PROPERTY_MAP.get(relationship_type, camel_case(relationship_type)))


def node_triples(node: dict) -> list[tuple[str, str]]:
    triples = [("a", ontology_ref(node["type"]))]

    for field in LITERAL_FIELDS:
        value = node.get(field)
        if value is None or value == "":
            continue
        triples.append((predicate_ref(field), ttl_string(value)))

    return triples


def format_subject(subject: str, triples: list[tuple[str, str]]) -> str:
    lines = [f"{subject}"]
    for index, (predicate, value) in enumerate(triples):
        ending = " ." if index == len(triples) - 1 else " ;"
        lines.append(f"    {predicate} {value}{ending}")
    return "\n".join(lines)


def build_turtle(graph: dict) -> str:
    lines = [
        f"@prefix {ENTITY_PREFIX}: <{BASE_IRI}entity/> .",
        f"@prefix {ONTOLOGY_PREFIX}: <{BASE_IRI}ontology/> .",
        "",
    ]

    for node in graph["nodes"]:
        lines.append(format_subject(entity_ref(node["id"]), node_triples(node)))
        lines.append("")

    relationship_groups: dict[str, list[tuple[str, str]]] = {}
    for relationship in graph["relationships"]:
        subject = entity_ref(relationship["source"])
        relationship_groups.setdefault(subject, []).append(
            (
                relationship_predicate(relationship["type"]),
                entity_ref(relationship["target"]),
            )
        )

    for subject in sorted(relationship_groups):
        triples = sorted(relationship_groups[subject])
        lines.append(format_subject(subject, triples))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    graph = load_graph()
    RDF_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_RDF_DIR.mkdir(parents=True, exist_ok=True)
    turtle = build_turtle(graph)
    TTL_PATH.write_text(turtle, encoding="utf-8")
    DOCS_TTL_PATH.write_text(turtle, encoding="utf-8")
    print(f"Wrote {TTL_PATH.relative_to(ROOT)}")
    print(f"Wrote {DOCS_TTL_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
