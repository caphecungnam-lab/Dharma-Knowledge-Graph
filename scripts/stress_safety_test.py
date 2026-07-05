from __future__ import annotations

import json

from dkg_api.app.observability.logger import get_logger
from dkg_api.app.safety.context_sanitizer import ContextSanitizer
from dkg_api.app.safety.output_validator import OutputValidator
from dkg_api.app.services.ai_reasoner import AIReasoner
from dkg_api.app.services.epistemic_truth_system import EpistemicTruthSystem


def main() -> int:
    logger = get_logger(__name__)
    unsafe_context = [
        {
            "match": {
                "node_id": "contradictory_node",
                "score": 0.8,
                "text": "All traditions agree despite contradiction.",
                "tradition": "vajrayana",
                "source_id": "source_conflict_001",
                "source_type": "commentary",
            },
            "related": [
                {
                    "id": "theravada_death",
                    "tradition": "theravada",
                    "definition": "contradicts another doctrinal interpretation",
                }
            ],
        },
        {
            "match": {
                "node_id": "missing_source_node",
                "score": 0.9,
                "text": "Missing source claim.",
                "tradition": "theravada",
            },
            "related": [],
        },
        {
            "match": {
                "node_id": "low_confidence_node",
                "score": 0.1,
                "text": "Low confidence claim.",
                "tradition": "theravada",
                "source_id": "source_low_001",
            },
            "related": [],
        },
    ]
    evaluated = EpistemicTruthSystem().evaluate(unsafe_context)
    sanitized = ContextSanitizer().sanitize(
        evaluated,
        allowed_layers=["core_fact", "doctrinal", "interpretive", "esoteric"],
    )
    answer = AIReasoner().generate("stress safety", sanitized)
    validation = OutputValidator().validate(answer, sanitized)
    rejected = len(sanitized) < len(evaluated) or validation["status"] == "REJECTED"
    payload = {
        "status": "ok" if rejected else "fail",
        "evaluated_nodes": len(evaluated),
        "accepted_nodes": len(sanitized),
        "rejected_nodes": len(evaluated) - len(sanitized),
        "output_validation": validation,
    }
    logger.info(
        "stress safety result status=%s rejected_nodes=%s validation=%s",
        payload["status"],
        payload["rejected_nodes"],
        validation,
    )
    print(json.dumps(payload, indent=2))
    return 0 if payload["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
