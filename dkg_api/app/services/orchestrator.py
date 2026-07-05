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
        answer.update(self._graph_response(query, context))
        return answer

    def _assert_allowed_dependency(self, dependency: Any) -> None:
        cls = dependency.__class__
        module_name = str(getattr(cls, "__module__", ""))
        class_name = str(getattr(cls, "__name__", ""))
        if class_name in self.FORBIDDEN_DEPENDENCY_NAMES:
            raise HardSafetyBlock("direct_database_or_ingestion_access_blocked")
        if any(fragment in module_name for fragment in self.FORBIDDEN_MODULE_FRAGMENTS):
            raise HardSafetyBlock("direct_database_or_ingestion_access_blocked")

    def _graph_response(
        self,
        query: str,
        context: list[dict[str, Any]],
    ) -> dict[str, object]:
        nodes_by_id: dict[str, dict[str, object]] = {}
        edges: list[dict[str, str]] = []

        for node in context:
            match = node.get("match") or {}
            node_id = str(node.get("node_id") or match.get("node_id") or "")
            if not node_id:
                continue
            nodes_by_id[node_id] = {
                "id": node_id,
                "label": str(match.get("label") or node_id),
                "type": str(node.get("epistemic_type") or "unknown"),
                "confidence": float(node.get("confidence") or 0.0),
            }
            for related in node.get("related") or []:
                related_id = str(related.get("id") or related.get("node_id") or "")
                if not related_id:
                    continue
                nodes_by_id.setdefault(
                    related_id,
                    {
                        "id": related_id,
                        "label": str(related.get("label") or related_id),
                        "type": str(related.get("epistemic_type") or "unknown"),
                        "confidence": float(related.get("confidence") or 0.5),
                    },
                )
                edges.append({"from": node_id, "to": related_id})

        return {
            "nodes": list(nodes_by_id.values()),
            "edges": edges,
            "center_node": self._center_node(query, list(nodes_by_id)),
            "epistemic_layers": self._epistemic_layers(list(nodes_by_id.values())),
            "confidence_map": {
                str(node["id"]): float(node["confidence"])
                for node in nodes_by_id.values()
            },
            "sanitized_context": context,
        }

    def _center_node(self, query: str, node_ids: list[str]) -> str:
        normalized_query = query.lower()
        for node_id in node_ids:
            if node_id.lower() in normalized_query:
                return node_id
        return node_ids[0] if node_ids else ""

    def _epistemic_layers(
        self,
        nodes: list[dict[str, object]],
    ) -> dict[str, list[str]]:
        layers: dict[str, list[str]] = {}
        for node in nodes:
            layer = str(node.get("type") or "unknown")
            layers.setdefault(layer, []).append(str(node["id"]))
        return layers
