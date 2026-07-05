from __future__ import annotations

import unittest
from pathlib import Path

from dkg_api.app.observability.metrics import MetricsCollector


ROOT = Path(__file__).resolve().parents[1]


class ProductionDeploymentTest(unittest.TestCase):
    def test_production_docker_compose_contains_required_services(self):
        content = (ROOT / "docker/docker-compose.prod.yml").read_text()

        for service in ("api:", "neo4j:", "qdrant:", "redis:", "prometheus:", "grafana:"):
            self.assertIn(service, content)
        self.assertNotIn('"7474:7474"', content)
        self.assertNotIn('"7687:7687"', content)
        self.assertNotIn('"6333:6333"', content)

    def test_deploy_workflow_runs_safety_tests_before_deploy(self):
        content = (ROOT / ".github/workflows/deploy.yml").read_text()

        self.assertIn("make check", content)
        self.assertIn("tests/test_safety_architecture.py", content)
        self.assertIn("amazon-ecs-deploy-task-definition", content)

    def test_metrics_collector_exports_required_json_shape(self):
        collector = MetricsCollector()
        collector.record_latency(10)
        collector.record_query("karma")
        collector.record_truth_filtering(evaluated_count=2, sanitized_count=1)

        health = collector.health_metrics()
        metrics = collector.metrics()

        self.assertIn("latency_avg_ms", health)
        self.assertIn("truth_rejection_rate", health)
        self.assertIn("top_queried_concepts", metrics)

    def test_prometheus_output_contains_core_metrics(self):
        collector = MetricsCollector()

        output = collector.prometheus(cache_hit_rate=0.5)

        self.assertIn("dkg_request_latency_avg_ms", output)
        self.assertIn("dkg_truth_rejection_rate", output)
        self.assertIn("dkg_cache_hit_rate 0.5", output)


if __name__ == "__main__":
    unittest.main()
