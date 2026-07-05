from __future__ import annotations

import json

import day1_graph_health
import day1_latency_baseline
import day1_retrieval_audit
import day1_safety_audit
import day1_system_health_check
import day1_truth_engine_snapshot
from day1_common import write_report

REPORT_PATH = "reports/day1_report.json"


def collect() -> dict[str, object]:
    health = day1_system_health_check.collect()
    latency = day1_latency_baseline.collect()
    retrieval = day1_retrieval_audit.collect()
    safety = day1_safety_audit.collect()
    graph = day1_graph_health.collect()
    truth = day1_truth_engine_snapshot.collect()

    risk_flags = []
    bottlenecks = []
    if health["system_status"] != "stable":
        risk_flags.append("one_or_more_core_health_checks_failed")
    if safety["status"] != "ok":
        risk_flags.append("safety_bypass_detected")
    if graph.get("status") != "ok":
        risk_flags.append("graph_health_unavailable")
    if graph.get("invalid_nodes", 0):
        risk_flags.append("graph_contains_nodes_missing_source_id")
    if retrieval.get("avg_rejection_rate", 0.0) > 0.5:
        risk_flags.append("high_truth_rejection_rate")

    bottleneck_stage = latency.get("bottleneck_stage")
    if bottleneck_stage and bottleneck_stage != "other":
        bottlenecks.append(bottleneck_stage)

    system_status = "stable"
    if risk_flags:
        system_status = "unstable"
    if safety["status"] == "critical_failure":
        system_status = "critical"

    return {
        "system_status": system_status,
        "latency_baseline": latency,
        "retrieval_health": retrieval,
        "safety_health": safety,
        "graph_health": graph,
        "truth_engine_health": truth,
        "bottlenecks": bottlenecks,
        "risk_flags": risk_flags,
    }


def main() -> int:
    payload = collect()
    write_report(REPORT_PATH, payload)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["system_status"] == "stable" else 1


if __name__ == "__main__":
    raise SystemExit(main())
