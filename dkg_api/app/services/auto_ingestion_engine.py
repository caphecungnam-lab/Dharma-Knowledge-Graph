from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from dkg_api.app.services.contradiction_miner import ContradictionMiner
from dkg_api.app.services.epistemic_truth_system import EpistemicTruthSystem
from dkg_api.app.services.graph_expander import GraphExpander
from dkg_api.app.services.knowledge_extractor import KnowledgeExtractor

if TYPE_CHECKING:
    from dkg_api.app.services.graph_service import GraphService


class AutoIngestionEngine:
    def __init__(self, graph: GraphService) -> None:
        self.graph = graph
        self.extractor = KnowledgeExtractor()
        self.truth_system = EpistemicTruthSystem()
        self.contradiction_miner = ContradictionMiner()
        self.graph_expander = GraphExpander(graph)

    def process_text(
        self,
        raw_text: str,
        source_metadata: dict[str, Any],
    ) -> dict[str, object]:
        chunks = self.extractor.split_into_chunks(raw_text)
        extracted = self.extractor.extract_candidates(chunks, source_metadata)
        contexts = [self._candidate_to_context(node) for node in extracted["nodes"]]
        evaluated = self.truth_system.evaluate(contexts)
        validated = self.truth_system.filter_ai_usable(evaluated)
        contradictions = self.contradiction_miner.mine(extracted["nodes"])
        expansion = self.graph_expander.expand(
            validated,
            relations=extracted["relations"],
            contradictions=contradictions,
        )

        return {
            "chunks": chunks,
            "candidates": extracted["nodes"],
            "validated_nodes": validated,
            "graph_expansion": expansion,
        }

    def _candidate_to_context(self, candidate: dict[str, Any]) -> dict[str, object]:
        return {
            "match": {
                "node_id": candidate["node_id"],
                "node_type": candidate["node_type"],
                "label": candidate["label"],
                "definition": candidate["definition"],
                "score": candidate["score"],
                "text": candidate["text"],
                "tradition": candidate["tradition"],
                "source_id": candidate["source_id"],
                "source_type": candidate["source_type"],
                "chunk_id": candidate["chunk_id"],
            },
            "related": [],
        }
