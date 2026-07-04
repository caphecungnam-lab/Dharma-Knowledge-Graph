from __future__ import annotations

from typing import Any


class PathfindingEngine:
    def build_path(
        self,
        raw_path: list[dict[str, Any]],
    ) -> list[dict[str, object]]:
        path = []
        for step in raw_path:
            path.append(
                {
                    "from": str(step.get("from") or ""),
                    "to": str(step.get("to") or ""),
                    "relation_type": str(step.get("type") or "RELATED_TO"),
                    "epistemic_confidence": float(step.get("confidence") or 0.5),
                    "tradition_relevance": str(step.get("tradition") or "shared_core"),
                }
            )
        return path
