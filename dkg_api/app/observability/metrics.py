from __future__ import annotations

from collections import Counter, deque
from statistics import mean
from typing import Any


class MetricsCollector:
    def __init__(self, latency_window: int = 500) -> None:
        self.latencies_ms: deque[float] = deque(maxlen=latency_window)
        self.step_latencies_ms: Counter[str] = Counter()
        self.step_counts: Counter[str] = Counter()
        self.truth_rejections = 0
        self.rejected_nodes = 0
        self.total_nodes_seen = 0
        self.confidence_buckets: Counter[str] = Counter()
        self.epistemic_distribution: Counter[str] = Counter()
        self.top_queries: Counter[str] = Counter()
        self.conflict_frequency: Counter[str] = Counter()

    def record_query(self, query: str) -> None:
        self.top_queries[query.lower().strip()] += 1

    def record_latency(self, milliseconds: float) -> None:
        self.latencies_ms.append(milliseconds)

    def record_step_latency(self, step: str, milliseconds: float) -> None:
        self.step_latencies_ms[step] += milliseconds
        self.step_counts[step] += 1

    def record_truth_filtering(
        self,
        evaluated_count: int,
        sanitized_count: int,
    ) -> None:
        rejected = max(evaluated_count - sanitized_count, 0)
        self.rejected_nodes += rejected
        self.total_nodes_seen += evaluated_count
        if rejected:
            self.truth_rejections += 1

    def record_context(self, context: list[dict[str, Any]]) -> None:
        for node in context:
            self.epistemic_distribution[str(node.get("epistemic_type") or "unknown")] += 1
            self.confidence_buckets[self._confidence_bucket(node)] += 1
            conflict = node.get("conflict") or {}
            conflict_type = str(conflict.get("type") or "none")
            self.conflict_frequency[conflict_type] += 1

    def health_metrics(self) -> dict[str, object]:
        truth_rejection_rate = (
            self.rejected_nodes / self.total_nodes_seen
            if self.total_nodes_seen
            else 0.0
        )
        return {
            "latency_avg_ms": round(mean(self.latencies_ms), 3)
            if self.latencies_ms
            else 0.0,
            "truth_rejection_rate": round(truth_rejection_rate, 3),
            "rejected_nodes": self.rejected_nodes,
            "queries_observed": sum(self.top_queries.values()),
        }

    def metrics(self) -> dict[str, object]:
        return {
            "epistemic_distribution": dict(self.epistemic_distribution),
            "top_queried_concepts": self.top_queries.most_common(10),
            "conflict_frequency": dict(self.conflict_frequency),
            "confidence_distribution": dict(self.confidence_buckets),
            "step_latency_avg_ms": self._step_averages(),
        }

    def prometheus(self, cache_hit_rate: float = 0.0) -> str:
        health = self.health_metrics()
        lines = [
            "# HELP dkg_request_latency_avg_ms Average request latency in milliseconds.",
            "# TYPE dkg_request_latency_avg_ms gauge",
            f"dkg_request_latency_avg_ms {health['latency_avg_ms']}",
            "# HELP dkg_truth_rejection_rate Ratio of evaluated nodes rejected by safety.",
            "# TYPE dkg_truth_rejection_rate gauge",
            f"dkg_truth_rejection_rate {health['truth_rejection_rate']}",
            "# HELP dkg_cache_hit_rate Query cache hit rate.",
            "# TYPE dkg_cache_hit_rate gauge",
            f"dkg_cache_hit_rate {cache_hit_rate}",
            "# HELP dkg_queries_observed Total observed AI queries.",
            "# TYPE dkg_queries_observed counter",
            f"dkg_queries_observed {health['queries_observed']}",
            "# HELP dkg_rejected_nodes Total rejected nodes.",
            "# TYPE dkg_rejected_nodes counter",
            f"dkg_rejected_nodes {health['rejected_nodes']}",
        ]
        for bucket, count in self.confidence_buckets.items():
            lines.append(
                f'dkg_ai_confidence_bucket{{bucket="{bucket}"}} {count}'
            )
        for epistemic_type, count in self.epistemic_distribution.items():
            lines.append(
                f'dkg_epistemic_distribution{{type="{epistemic_type}"}} {count}'
            )
        return "\n".join(lines) + "\n"

    def _confidence_bucket(self, node: dict[str, Any]) -> str:
        confidence = float(node.get("confidence") or 0.0)
        if confidence >= 0.9:
            return "high"
        if confidence >= 0.7:
            return "medium_high"
        if confidence >= 0.5:
            return "medium"
        return "low"

    def _step_averages(self) -> dict[str, float]:
        averages = {}
        for step, total in self.step_latencies_ms.items():
            count = self.step_counts[step]
            averages[step] = round(total / count, 3) if count else 0.0
        return averages


metrics = MetricsCollector()
