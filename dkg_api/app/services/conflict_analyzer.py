from __future__ import annotations

from typing import Any


class ConflictAnalyzer:
    def analyze(self, node: dict[str, Any]) -> dict[str, object]:
        text = self._combined_text(node)
        traditions = self._traditions(node)

        if any(
            marker in text
            for marker in ["ontology", "reality model", "ultimate reality"]
        ):
            return {"type": "ontological", "severity": 0.85}

        if any(marker in text for marker in ["contradict", "reject", "opposes"]):
            return {"type": "doctrinal", "severity": 0.7}

        if any(
            marker in text
            for marker in ["different wording", "same meaning", "synonym"]
        ):
            return {"type": "semantic", "severity": 0.25}

        if len(traditions) > 1 and any(
            marker in text for marker in ["interpretation", "commentary", "view"]
        ):
            return {"type": "doctrinal", "severity": 0.55}

        return {"type": "none", "severity": 0.0}

    def _combined_text(self, node: dict[str, Any]) -> str:
        match = node.get("match", {})
        values = [
            str(match.get("text") or ""),
            str(match.get("label") or ""),
            str(match.get("definition") or ""),
        ]
        for related in node.get("related", []):
            values.extend(
                [
                    str(related.get("label") or ""),
                    str(related.get("definition") or ""),
                ]
            )
        return " ".join(values).lower()

    def _traditions(self, node: dict[str, Any]) -> set[str]:
        match = node.get("match", {})
        traditions = {str(match.get("tradition") or "").lower().strip()}
        for related in node.get("related", []):
            traditions.add(str(related.get("tradition") or "").lower().strip())
        return {tradition for tradition in traditions if tradition}
