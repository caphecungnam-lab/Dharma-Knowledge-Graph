from __future__ import annotations

from typing import Any

from dkg_api.app.observability.metrics import metrics
from dkg_api.app.observability.trace import trace_step
from dkg_api.app.safety.context_sanitizer import ContextSanitizer
from dkg_api.app.safety.epistemic_boundary import EpistemicBoundary
from dkg_api.app.safety.epistemic_gateway import EpistemicGateway
from dkg_api.app.safety.injection_guard import InjectionGuard
from dkg_api.app.safety.output_validator import OutputValidator
from dkg_api.app.safety.retrieval_control_layer import RetrievalControlLayer
from dkg_api.app.safety.safety_policy import critical_safety_failure, rejected_response
from dkg_api.app.services.context_reduction_engine import ContextReductionEngine
from dkg_api.app.services.epistemic_truth_system import EpistemicTruthSystem


class SafetyOrchestrator:
    def __init__(self) -> None:
        self.injection_guard = InjectionGuard()
        self.gateway = EpistemicGateway()
        self.retrieval = RetrievalControlLayer()
        self.truth_system = EpistemicTruthSystem()
        self.sanitizer = ContextSanitizer()
        self.boundary = EpistemicBoundary()
        self.reducer = ContextReductionEngine()
        self.output_validator = OutputValidator()

    def prepare_context(
        self,
        query: str,
        *,
        vector: Any,
        graph: Any,
    ) -> dict[str, object]:
        injection = self.injection_guard.inspect(query)
        if injection["status"] != "ok":
            return critical_safety_failure("injection_guard", "prompt_injection_detected")

        with trace_step("epistemic_gateway"):
            classification = self.gateway.classify_query(query)
        if classification["mode"] == "reject":
            return rejected_response(
                ["accepted_query_mode"],
                safety={
                    "gateway": classification,
                    "stopped_at": "epistemic_gateway",
                },
            )

        with trace_step("retrieval"):
            graph_vector_context = self.retrieval.fetch(query, vector, graph)

        try:
            with trace_step("truth_engine"):
                evaluations = self.truth_system.evaluate(graph_vector_context)
        except Exception:
            return critical_safety_failure("truth_engine", "truth_engine_unavailable")

        with trace_step("context_sanitizer"):
            validated_context = self.sanitizer.sanitize(
                self.truth_system.filter_ai_usable(evaluations),
                allowed_layers=classification["allowed_layers"],
            )
        metrics.record_truth_filtering(len(evaluations), len(validated_context))
        if not validated_context:
            return rejected_response(
                ["sanitized_epistemic_context"],
                safety={
                    "gateway": classification,
                    "stopped_at": "context_sanitizer",
                },
            )

        boundary = self.boundary.enforce(validated_context)
        if boundary["status"] != "ok":
            return boundary

        with trace_step("context_reduction"):
            reduced_context = self.reducer.reduce(
                list(boundary.get("context") or validated_context)
            )
        metrics.record_context(reduced_context)

        return {
            "status": "ok",
            "gateway": classification,
            "context": reduced_context,
            "evaluated_count": len(evaluations),
            "sanitized_count": len(reduced_context),
        }

    def validate_output(
        self,
        answer: dict[str, Any],
        context: list[dict[str, Any]],
    ) -> dict[str, object]:
        boundary = self.boundary.validate_answer(answer, context)
        if boundary["status"] != "ok":
            return boundary
        validation = self.output_validator.validate(answer, context)
        if validation["status"] != "APPROVED":
            return rejected_response(
                list(validation["errors"]),
                safety={
                    "output_validation": validation,
                    "stopped_at": "output_validator",
                },
            )
        return {"status": "ok", "output_validation": validation}
