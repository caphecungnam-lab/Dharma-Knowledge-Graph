from __future__ import annotations

import uuid
from pathlib import Path
from typing import TYPE_CHECKING, Any

from dkg_api.app.ingestion.corpus_loader import CorpusLoader
from dkg_api.app.ingestion.deduplication_engine import DeduplicationEngine
from dkg_api.app.ingestion.entity_normalizer import EntityNormalizer
from dkg_api.app.ingestion.knowledge_extractor import KnowledgeExtractor
from dkg_api.app.ingestion.text_chunker import TextChunker
from dkg_api.app.ingestion.validation_layer import validate_ingested_node
from dkg_api.app.services.embedding_service import embed_text
from dkg_api.app.services.epistemic_truth_system import EpistemicTruthSystem
from dkg_api.app.services.graph_expander import GraphExpander

if TYPE_CHECKING:
    from dkg_api.app.services.graph_service import GraphService
    from dkg_api.app.services.vector_service import VectorService


class IngestionPipeline:
    def __init__(
        self,
        graph: GraphService,
        vector: VectorService,
        loader: CorpusLoader | None = None,
        chunker: TextChunker | None = None,
        extractor: KnowledgeExtractor | None = None,
        normalizer: EntityNormalizer | None = None,
        truth_system: EpistemicTruthSystem | None = None,
        deduplication: DeduplicationEngine | None = None,
    ) -> None:
        self.graph = graph
        self.vector = vector
        self.loader = loader or CorpusLoader()
        self.chunker = chunker or TextChunker()
        self.extractor = extractor or KnowledgeExtractor()
        self.normalizer = normalizer or EntityNormalizer()
        self.truth_system = truth_system or EpistemicTruthSystem()
        self.deduplication = deduplication or DeduplicationEngine()
        self.expander = GraphExpander(graph)

    def run(
        self,
        file_path: str | Path,
        source_metadata: dict[str, Any],
    ) -> dict[str, Any]:
        doc = self.loader.load(file_path, source_metadata)
        metadata = doc["source_metadata"]
        chunks = self.chunker.chunk(doc["text"], source_id=metadata["source_id"])
        if not chunks:
            return {
                "status": "rejected",
                "stage": "chunk",
                "reason": "epistemic_uncertainty",
                "chunk_id": None,
            }
        malformed = self._malformed_chunk(chunks)
        if malformed is not None:
            return {
                "status": "rejected",
                "stage": "chunk",
                "reason": "schema_violation",
                "chunk_id": malformed.get("chunk_id"),
            }

        self._store_chunks(chunks, metadata)
        all_candidates: list[dict[str, Any]] = []
        all_relations: list[dict[str, str]] = []
        rejected_chunks = []
        deduplication_reports = []

        for chunk in chunks:
            try:
                extracted = self.extractor.extract(chunk, metadata)
            except Exception as error:
                return {
                    "status": "rejected",
                    "stage": "extract",
                    "reason": str(error),
                    "chunk_id": chunk.get("chunk_id"),
                }
            normalized = self.normalizer.normalize(extracted)
            deduplication_reports.append(
                self.deduplication.analyze(normalized.get("concepts", []))
            )
            candidates = self._graph_candidates(normalized, chunk, metadata)
            if not candidates:
                rejected_chunks.append(
                    {
                        "status": "rejected",
                        "stage": "extract",
                        "reason": "epistemic_uncertainty",
                        "chunk_id": chunk["chunk_id"],
                    }
                )
                continue

            pre_validated = []
            for candidate in candidates:
                validation = validate_ingested_node(candidate)
                if validation["status"] != "ok":
                    rejected_chunks.append(
                        {
                            "status": "rejected",
                            "stage": "validate",
                            "reason": validation["reason"],
                            "chunk_id": chunk["chunk_id"],
                            "node_id": validation.get("node_id"),
                        }
                    )
                    continue
                pre_validated.append(candidate)
            if not pre_validated:
                continue

            evaluated = self.truth_system.evaluate(pre_validated)
            allowed = [
                node
                for node in evaluated
                if node.get("ai_usage_allowed") is True
                and float(node.get("confidence") or 0.0) >= 0.5
            ]
            if not allowed:
                rejected_chunks.append(
                    {
                        "status": "rejected",
                        "stage": "validate",
                        "reason": "epistemic_uncertainty",
                        "chunk_id": chunk["chunk_id"],
                    }
                )
                continue

            all_candidates.extend(allowed)
            all_relations.extend(self._candidate_relations(normalized))

        expanded = self.expander.expand(all_candidates, all_relations)
        write_failures = expanded.get("rejected_writes", [])
        return {
            "status": "ok" if expanded["inserted_nodes"] else "rejected",
            "source_id": metadata["source_id"],
            "chunks": len(chunks),
            "stored_chunks": len(chunks),
            "validated_nodes": len(all_candidates),
            "inserted_nodes": expanded["inserted_nodes"],
            "inserted_relations": expanded["inserted_relations"],
            "rejections": rejected_chunks + list(write_failures),
            "deduplication": self._merge_deduplication_reports(deduplication_reports),
        }

    def _store_chunks(
        self,
        chunks: list[dict[str, Any]],
        metadata: dict[str, Any],
    ) -> None:
        points = []
        for chunk in chunks:
            chunk_id = str(chunk["chunk_id"])
            payload = {
                "node_id": chunk_id,
                "chunk_text": chunk["text"],
                "text": chunk["text"],
                "chunk_id": chunk_id,
                "source_id": metadata["source_id"],
                "tradition": metadata["tradition"],
                "source_type": metadata["source_type"],
                "title": metadata["title"],
            }
            points.append(
                {
                    "point_id": str(uuid.uuid5(uuid.NAMESPACE_URL, f"dkg:{chunk_id}")),
                    "vector": embed_text(str(chunk["text"])),
                    "payload": payload,
                }
            )
        self.vector.client.upsert_points(points)

    def _graph_candidates(
        self,
        normalized: dict[str, list[dict[str, Any]]],
        chunk: dict[str, Any],
        metadata: dict[str, Any],
    ) -> list[dict[str, Any]]:
        candidates = []
        for concept in normalized.get("concepts", []):
            candidates.append(
                {
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
                        "epistemic_type": self._provisional_epistemic_type(
                            concept,
                            metadata,
                        ),
                    },
                    "related": [],
                }
            )
        return candidates

    def _candidate_relations(
        self,
        normalized: dict[str, list[dict[str, Any]]],
    ) -> list[dict[str, str]]:
        label_to_id = {
            concept["label"]: concept["id"]
            for concept in normalized.get("concepts", [])
        }
        relations = []
        for relation in normalized.get("relations", []):
            source_id = label_to_id.get(relation["from"])
            target_id = label_to_id.get(relation["to"])
            if source_id and target_id:
                relations.append(
                    {
                        "source": source_id,
                        "target": target_id,
                        "type": relation.get("type") or "MENTIONS",
                    }
                )
        return relations

    def _provisional_epistemic_type(
        self,
        concept: dict[str, Any],
        metadata: dict[str, Any],
    ) -> str:
        text = str(concept.get("definition") or "").lower()
        if metadata.get("source_type") == "sutta":
            return "core_fact"
        if metadata.get("tradition") == "vajrayana" or "bardo" in text or "tantra" in text:
            return "esoteric"
        return "doctrinal"

    def _malformed_chunk(
        self,
        chunks: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        for chunk in chunks:
            if not chunk.get("chunk_id") or not str(chunk.get("text") or "").strip():
                return chunk
        return None

    def _merge_deduplication_reports(
        self,
        reports: list[dict[str, list[dict[str, Any]]]],
    ) -> dict[str, list[dict[str, Any]]]:
        merged = {
            "duplicates": [],
            "conflicts": [],
            "merged_suggestions": [],
        }
        for report in reports:
            for key in merged:
                merged[key].extend(report.get(key, []))
        return merged
