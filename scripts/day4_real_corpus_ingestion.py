#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import uuid
from collections import Counter
from pathlib import Path
from typing import Any

from dkg_api.app.db.graph_write_guard import GraphWriteGuard
from dkg_api.app.ingestion.day4_extractor import Day4Extractor
from dkg_api.app.ingestion.entity_normalizer import EntityNormalizer
from dkg_api.app.ingestion.text_chunker import TextChunker
from dkg_api.app.ingestion.validation_layer import validate_ingested_node
from dkg_api.app.services.embedding_service import embed_text
from dkg_api.app.services.epistemic_truth_system import EpistemicTruthSystem


DEFAULT_SOURCE = Path("data/raw/giac_khang/FISpARohzy8/source.vi.vtt")
DEFAULT_REPORT = Path("reports/day4_corpus_report.json")


class Day4VectorSink:
    def __init__(self) -> None:
        self.points: list[dict[str, Any]] = []

    def upsert_points(self, points: list[dict[str, Any]]) -> None:
        self.points.extend(points)


class Day4GraphSink:
    def __init__(self) -> None:
        self.nodes: list[dict[str, Any]] = []
        self.source_links: list[dict[str, Any]] = []
        self.relationships: list[dict[str, Any]] = []
        self.contradictions: list[dict[str, Any]] = []

    def upsert_generated_node(self, node: dict[str, Any]) -> None:
        self.nodes.append(node)

    def link_source_chunk(self, node: dict[str, Any]) -> None:
        self.source_links.append(node)

    def create_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship_type: str,
    ) -> None:
        self.relationships.append(
            {
                "source": source_id,
                "target": target_id,
                "type": relationship_type,
            }
        )

    def create_contradiction(self, contradiction: dict[str, Any]) -> None:
        self.contradictions.append(contradiction)


def run_ingestion(
    sources: list[dict[str, Any]],
    *,
    chunk_limit: int | None = None,
) -> dict[str, Any]:
    graph = Day4GraphSink()
    vector = Day4VectorSink()
    guard = GraphWriteGuard(graph)
    extractor = Day4Extractor()
    normalizer = EntityNormalizer()
    truth = EpistemicTruthSystem()

    documents = []
    all_rejections = []
    all_conflicts = []
    accepted_nodes = []
    total_chunks = 0

    for source in sources:
        try:
            document_result = process_source(
                source,
                extractor=extractor,
                normalizer=normalizer,
                truth=truth,
                guard=guard,
                vector=vector,
                chunk_limit=chunk_limit,
            )
        except Exception as error:
            document_result = rejected_error(
                "corpus",
                str(error),
                source.get("source_id", "unknown"),
            )

        documents.append(document_result)
        total_chunks += int(document_result.get("chunks_created") or 0)
        all_rejections.extend(document_result.get("rejections", []))
        all_conflicts.extend(document_result.get("conflicts", []))
        accepted_nodes.extend(document_result.get("accepted_nodes", []))

    report = {
        "status": "ok" if accepted_nodes else "rejected",
        "total_documents_processed": len(documents),
        "total_chunks_created": total_chunks,
        "nodes_accepted": len(accepted_nodes),
        "nodes_rejected": len(all_rejections),
        "rejection_reasons": dict(Counter(item.get("reason") for item in all_rejections)),
        "conflict_clusters_detected": all_conflicts,
        "drift_signals_detected": drift_from_nodes(accepted_nodes),
        "documents": documents,
        "vector_points": len(vector.points),
        "graph_nodes_written": len(graph.nodes),
        "graph_relationships_written": len(graph.relationships),
    }
    return report


def process_source(
    source: dict[str, Any],
    *,
    extractor: Day4Extractor,
    normalizer: EntityNormalizer,
    truth: EpistemicTruthSystem,
    guard: GraphWriteGuard,
    vector: Day4VectorSink,
    chunk_limit: int | None,
) -> dict[str, Any]:
    metadata = normalized_metadata(source)
    text = load_real_source(Path(source["path"]))
    chunks = TextChunker(max_tokens=700).chunk(text, source_id=metadata["source_id"])
    if chunk_limit is not None:
        chunks = chunks[:chunk_limit]
    if not chunks:
        return rejected_error("chunking", "no_chunks_created", metadata["source_id"])

    vector.upsert_points([chunk_point(chunk, metadata) for chunk in chunks])

    accepted_nodes = []
    rejections = []
    conflicts = []
    relation_candidates = []

    for chunk in chunks:
        extracted = extractor.extract(chunk, metadata)
        normalized = normalizer.normalize(extracted)
        concepts = normalized.get("concepts", [])
        if not concepts:
            rejections.append(
                rejected_error(
                    "extraction",
                    "no_explicit_concept",
                    metadata["source_id"],
                    chunk_id=str(chunk["chunk_id"]),
                )
            )
            continue

        candidates = [candidate_node(concept, metadata, chunk) for concept in concepts]
        pre_validated = []
        for candidate in candidates:
            validation = validate_ingested_node(candidate)
            if validation["status"] != "ok":
                rejections.append(
                    rejected_error(
                        "validation",
                        str(validation["reason"]),
                        metadata["source_id"],
                        node_id=str(validation.get("node_id") or ""),
                        chunk_id=str(chunk["chunk_id"]),
                    )
                )
                continue
            pre_validated.append(candidate)

        evaluated = truth.evaluate(pre_validated)
        for node in evaluated:
            if node.get("ai_usage_allowed") is not True:
                rejections.append(
                    rejected_error(
                        "validation",
                        "epistemic_uncertainty",
                        metadata["source_id"],
                        node_id=str(node.get("node_id") or ""),
                        chunk_id=str(chunk["chunk_id"]),
                    )
                )
                continue
            write_result = guard.write_node(node)
            if write_result["status"] != "ok":
                rejections.append(
                    rejected_error(
                        "graph_write",
                        str(write_result.get("reason") or "write_rejected"),
                        metadata["source_id"],
                        node_id=str(write_result.get("node_id") or ""),
                        chunk_id=str(chunk["chunk_id"]),
                    )
                )
                continue
            accepted_nodes.append(node)

        relation_candidates.extend(normalized.get("relations", []))
        conflicts.extend(conflicts_from_concepts(concepts))

    return {
        "status": "ok" if accepted_nodes else "rejected",
        "source_id": metadata["source_id"],
        "title": metadata["title"],
        "tradition": metadata["tradition"],
        "language": metadata["language"],
        "chunks_created": len(chunks),
        "accepted_nodes": accepted_nodes,
        "accepted_node_ids": [node["node_id"] for node in accepted_nodes],
        "rejections": rejections,
        "relations_detected": relation_candidates,
        "conflicts": conflicts,
    }


def load_real_source(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"real corpus source not found: {path}")
    suffix = path.suffix.lower()
    if suffix == ".vtt":
        return clean_vtt(path.read_text(encoding="utf-8"))
    if suffix in {".txt", ".md"}:
        return clean_text(path.read_text(encoding="utf-8"))
    if suffix == ".json":
        return clean_text(text_from_json(path))
    if suffix == ".pdf":
        return clean_text(text_from_pdf(path))
    raise ValueError(f"unsupported real corpus file type: {suffix}")


def clean_vtt(raw: str) -> str:
    lines = []
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped == "WEBVTT":
            continue
        if stripped.startswith(("Kind:", "Language:")):
            continue
        if "-->" in stripped:
            continue
        cleaned = re.sub(r"<[^>]+>", "", stripped)
        cleaned = re.sub(r"\d{2}:\d{2}:\d{2}\.\d{3}", "", cleaned)
        cleaned = clean_text(cleaned)
        if cleaned:
            lines.append(cleaned)
    return clean_text(" ".join(dedupe_adjacent(lines)))


def clean_text(text: str) -> str:
    text = text.replace("\ufeff", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def dedupe_adjacent(lines: list[str]) -> list[str]:
    deduped = []
    previous = ""
    for line in lines:
        if line == previous:
            continue
        deduped.append(line)
        previous = line
    return deduped


def text_from_json(path: Path) -> str:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        if payload.get("text") or payload.get("transcript"):
            return str(payload.get("text") or payload.get("transcript"))
        if isinstance(payload.get("segments"), list):
            return " ".join(str(item.get("text") or "") for item in payload["segments"])
    raise ValueError(f"json source does not contain text: {path}")


def text_from_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except Exception as error:
        raise RuntimeError("PDF ingestion requires pypdf.") from error
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def normalized_metadata(source: dict[str, Any]) -> dict[str, str]:
    required = {"source_id", "title", "tradition", "author", "language"}
    missing = sorted(field for field in required if not source.get(field))
    if missing:
        raise ValueError(f"missing metadata fields: {missing}")
    return {
        "source_id": str(source["source_id"]),
        "title": str(source["title"]),
        "tradition": str(source["tradition"]).lower(),
        "author": str(source["author"]),
        "language": str(source["language"]),
        "source_type": str(source.get("source_type") or "dharma_talk"),
    }


def chunk_point(chunk: dict[str, Any], metadata: dict[str, str]) -> dict[str, Any]:
    chunk_id = str(chunk["chunk_id"])
    return {
        "point_id": str(uuid.uuid5(uuid.NAMESPACE_URL, f"dkg-day4:{chunk_id}")),
        "vector": embed_text(str(chunk["text"])),
        "payload": {
            "node_id": chunk_id,
            "chunk_id": chunk_id,
            "text": chunk["text"],
            "source_id": metadata["source_id"],
            "tradition": metadata["tradition"],
            "title": metadata["title"],
        },
    }


def candidate_node(
    concept: dict[str, Any],
    metadata: dict[str, str],
    chunk: dict[str, Any],
) -> dict[str, Any]:
    return {
        "match": {
            "node_id": concept["id"],
            "node_type": "Concept",
            "label": concept["label"],
            "definition": concept["definition"],
            "text": concept["definition"],
            "tradition": concept.get("tradition") or metadata["tradition"],
            "source_id": concept.get("source_id") or metadata["source_id"],
            "source_type": concept.get("source_type") or metadata["source_type"],
            "chunk_id": concept.get("chunk_id") or chunk["chunk_id"],
            "score": concept.get("score", 0.86),
            "epistemic_type": "doctrinal",
        },
        "related": [],
    }


def conflicts_from_concepts(concepts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id: dict[str, set[str]] = {}
    for concept in concepts:
        by_id.setdefault(str(concept.get("id")), set()).add(str(concept.get("definition")))
    return [
        {
            "concept": concept_id,
            "conflict_type": "definition_variation",
            "severity": 0.4,
        }
        for concept_id, definitions in by_id.items()
        if len(definitions) > 1
    ]


def drift_from_nodes(nodes: list[dict[str, Any]]) -> dict[str, Any]:
    by_concept: dict[str, dict[str, set[str]]] = {}
    for node in nodes:
        concept = str(node.get("node_id") or "")
        by_concept.setdefault(concept, {"traditions": set(), "types": set()})
        by_concept[concept]["traditions"].add(str(node.get("tradition") or "unknown"))
        by_concept[concept]["types"].add(str(node.get("epistemic_type") or "unknown"))

    affected = [
        concept
        for concept, values in by_concept.items()
        if len(values["traditions"]) > 1 or len(values["types"]) > 1
    ]
    return {
        "drift_detected": bool(affected),
        "affected_concepts": affected,
        "severity": "medium" if affected else "low",
    }


def rejected_error(
    stage: str,
    reason: str,
    source_id: str,
    *,
    node_id: str | None = None,
    chunk_id: str | None = None,
) -> dict[str, Any]:
    response: dict[str, Any] = {
        "status": "rejected",
        "stage": stage,
        "reason": reason,
        "source_id": source_id,
    }
    if node_id:
        response["node_id"] = node_id
    if chunk_id:
        response["chunk_id"] = chunk_id
    return response


def default_sources() -> list[dict[str, Any]]:
    return [
        {
            "path": str(DEFAULT_SOURCE),
            "source_id": "source_youtube_fisp_arohzy8",
            "title": "1A. KINH 6 6 L2CÂU 1 P1",
            "tradition": "theravada",
            "author": "HT. Thích Giác Khang",
            "language": "vi",
            "source_type": "dharma_talk",
        }
    ]


def parse_sources(args: argparse.Namespace) -> list[dict[str, Any]]:
    if args.manifest:
        payload = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        return list(payload.get("sources") or [])
    if args.source:
        return [
            {
                "path": args.source,
                "source_id": args.source_id,
                "title": args.title,
                "tradition": args.tradition,
                "author": args.author,
                "language": args.language,
                "source_type": args.source_type,
            }
        ]
    return default_sources()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source")
    parser.add_argument("--manifest")
    parser.add_argument("--source-id", default="source_day4_real")
    parser.add_argument("--title", default="Day 4 Real Corpus Source")
    parser.add_argument("--tradition", default="unknown")
    parser.add_argument("--author", default="unknown")
    parser.add_argument("--language", default="unknown")
    parser.add_argument("--source-type", default="text")
    parser.add_argument("--chunk-limit", type=int)
    parser.add_argument("--output", default=str(DEFAULT_REPORT))
    args = parser.parse_args()

    report = run_ingestion(parse_sources(args), chunk_limit=args.chunk_limit)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
