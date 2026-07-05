from __future__ import annotations

import json

from day1_common import distribution, sample_truth_nodes
from dkg_api.app.services.epistemic_truth_system import EpistemicTruthSystem


def collect() -> dict[str, object]:
    evaluated = EpistemicTruthSystem().evaluate(sample_truth_nodes())
    type_counts = distribution([node["epistemic_type"] for node in evaluated])
    allowed = [node for node in evaluated if node.get("ai_usage_allowed") is True]
    confidences = [float(node.get("confidence") or 0.0) for node in evaluated]
    return {
        "core_fact": type_counts.get("core_fact", 0),
        "doctrinal_view": type_counts.get("doctrinal_view", 0),
        "interpretive_view": type_counts.get("interpretive_view", 0),
        "esoteric_view": type_counts.get("esoteric_view", 0),
        "unknown": type_counts.get("unknown", 0),
        "confidence_distribution": confidences,
        "rejection_rate": round((len(evaluated) - len(allowed)) / len(evaluated), 3),
    }


def main() -> int:
    payload = collect()
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
