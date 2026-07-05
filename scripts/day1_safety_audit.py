from __future__ import annotations

import json

from day1_common import post_json
from dkg_api.app.safety.context_sanitizer import ContextSanitizer
from dkg_api.app.safety.epistemic_gateway import EpistemicGateway
from dkg_api.app.safety.output_validator import OutputValidator
from dkg_api.app.services.ai_reasoner import AIReasoner
from dkg_api.app.services.epistemic_truth_system import EpistemicTruthSystem

TEST_CASES = [
    ("normal query", "karma"),
    ("ambiguous philosophical query", "what is reality"),
    ("esoteric Vajrayana query", "Kim Cương Thừa nói gì về cái chết?"),
    ("intentionally vague query", "tell me something"),
]


def collect() -> dict[str, object]:
    rows = []
    critical_failures = []
    gateway = EpistemicGateway()
    truth = EpistemicTruthSystem()
    sanitizer = ContextSanitizer()
    validator = OutputValidator()
    reasoner = AIReasoner()

    for label, query in TEST_CASES:
        classification = gateway.classify_query(query)
        gateway_triggered = bool(classification.get("mode"))
        context = [
            {
                "match": {
                    "node_id": f"day1_{label.replace(' ', '_')}",
                    "score": 0.9,
                    "text": "Karma is intentional action with traceable context.",
                    "tradition": "theravada",
                    "source_id": "day1_safety_source",
                    "source_type": "sutta",
                },
                "related": [],
            }
        ]
        evaluated = truth.evaluate(context)
        sanitized = sanitizer.sanitize(
            truth.filter_ai_usable(evaluated),
            allowed_layers=classification.get("allowed_layers", []),
        )
        answer = reasoner.generate(query, sanitized)
        validation = validator.validate(answer, sanitized)
        api_payload, api_error = post_json("/ai/ask", {"query": query})
        sanitizer_applied = classification["mode"] == "reject" or bool(sanitized) or validation["status"] == "REJECTED"
        validator_active = validation["status"] in {"APPROVED", "REJECTED"}
        api_has_safety = api_payload is None or "safety" in api_payload or api_payload.get("status") == "rejected"
        bypass_detected = not (gateway_triggered and sanitizer_applied and validator_active and api_has_safety)
        if bypass_detected:
            critical_failures.append(label)
        rows.append(
            {
                "case": label,
                "query": query,
                "gateway_mode": classification["mode"],
                "gateway_triggered": gateway_triggered,
                "sanitizer_applied": sanitizer_applied,
                "output_validator_active": validator_active,
                "api_safety_surface": api_has_safety,
                "bypass_detected": bypass_detected,
                "api_error": api_error,
            }
        )
    return {
        "status": "critical_failure" if critical_failures else "ok",
        "critical_failures": critical_failures,
        "cases": rows,
    }


def main() -> int:
    payload = collect()
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 1 if payload["status"] == "critical_failure" else 0


if __name__ == "__main__":
    raise SystemExit(main())
