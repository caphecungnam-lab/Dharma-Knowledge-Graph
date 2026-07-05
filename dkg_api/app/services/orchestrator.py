from __future__ import annotations

from typing import Any

from dkg_api.app.observability.metrics import metrics
from dkg_api.app.observability.trace import trace_step
from dkg_api.app.safety.safety_orchestrator import SafetyOrchestrator
from dkg_api.app.services.ai_reasoner import AIReasoner


class HardSafetyBlock(RuntimeError):
    pass


class AIOrchestrator:
    FORBIDDEN_DEPENDENCY_NAMES = {
        "Neo4jClient",
        "QdrantClient",
        "IngestionPipeline",
    }
    FORBIDDEN_MODULE_FRAGMENTS = {
        ".db.neo4j_client",
        ".db.qdrant_client",
        ".ingestion.ingestion_pipeline",
    }

    def __init__(
        self,
        *,
        graph: Any,
        vector: Any,
        safety: SafetyOrchestrator | None = None,
        reasoner: AIReasoner | None = None,
    ) -> None:
        self._assert_allowed_dependency(graph)
        self._assert_allowed_dependency(vector)
        self.graph = graph
        self.vector = vector
        self.safety = safety or SafetyOrchestrator()
        self.reasoner = reasoner or AIReasoner()

    def answer(self, query: str) -> dict[str, object]:
        metrics.record_query(query)
        prepared = self.safety.prepare_context(
            query,
            vector=self.vector,
            graph=self.graph,
        )
        if prepared.get("status") != "ok":
            return prepared

        context = list(prepared["context"])
        with trace_step("ai_reasoner"):
            answer = self.reasoner.generate(query, context)
        validation = self.safety.validate_output(answer, context)
        if validation.get("status") != "ok":
            return validation

        answer["safety"] = {
            "gateway": prepared["gateway"],
            "output_validation": validation["output_validation"],
        }
        return answer

    def _assert_allowed_dependency(self, dependency: Any) -> None:
        cls = dependency.__class__
        module_name = str(getattr(cls, "__module__", ""))
        class_name = str(getattr(cls, "__name__", ""))
        if class_name in self.FORBIDDEN_DEPENDENCY_NAMES:
            raise HardSafetyBlock("direct_database_or_ingestion_access_blocked")
        if any(fragment in module_name for fragment in self.FORBIDDEN_MODULE_FRAGMENTS):
            raise HardSafetyBlock("direct_database_or_ingestion_access_blocked")
