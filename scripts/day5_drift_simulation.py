#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from dkg_api.app.observability.alerts import AlertEngine
from dkg_api.app.observability.conflict_map import ConflictMap
from dkg_api.app.observability.drift_detector import DriftDetector
from dkg_api.app.observability.epistemic_monitor import EpistemicMonitor


DEFAULT_OUTPUT = Path("reports/day5_drift_simulation.json")


def simulated_nodes() -> list[dict[str, Any]]:
    return [
        node(
            "concept_death",
            "theravada",
            "doctrinal_view",
            0.82,
            "Death is presented as dissolution of aggregates.",
        ),
        node(
            "concept_death",
            "vajrayana",
            "esoteric_view",
            0.78,
            "Death is presented as transition into bardo.",
            conflict_type="doctrinal",
        ),
        node(
            "concept_karma",
            "theravada",
            "core_fact",
            0.96,
            "Karma is intentional action.",
        ),
        node(
            "concept_karma",
            "mahayana",
            "interpretive_view",
            0.58,
            "Karma is described with a different interpretive emphasis.",
        ),
    ]


def node(
    node_id: str,
    tradition: str,
    epistemic_type: str,
    confidence: float,
    definition: str,
    *,
    conflict_type: str = "none",
) -> dict[str, Any]:
    return {
        "node_id": node_id,
        "tradition": tradition,
        "epistemic_type": epistemic_type,
        "confidence": confidence,
        "source_ids": [f"source_{tradition}_{node_id}"],
        "conflict": {
            "type": conflict_type,
            "severity": 0.7 if conflict_type != "none" else 0.0,
        },
        "match": {
            "node_id": node_id,
            "definition": definition,
            "text": definition,
            "chunk_id": f"chunk_{tradition}_{node_id}",
        },
    }


def run_simulation() -> dict[str, Any]:
    nodes = simulated_nodes()
    rejections = [
        {
            "status": "rejected",
            "reason": "epistemic_uncertainty",
            "node_id": "concept_untraceable",
        }
    ]
    monitor = EpistemicMonitor().snapshot(
        accepted_nodes=nodes,
        rejections=rejections,
    )
    drift = DriftDetector().detect(nodes)
    conflicts = ConflictMap().build(nodes)
    alerts = AlertEngine().evaluate(
        monitor_snapshot=monitor,
        drift=drift,
    )
    return {
        "status": "ok",
        "drift": drift,
        "monitor": monitor,
        "conflict_map": conflicts,
        "alerts": alerts,
        "merge_policy": "conflicts_visible_not_merged",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    report = run_simulation()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
