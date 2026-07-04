from __future__ import annotations

from typing import Any

TRADITIONS = {"theravada", "mahayana", "vajrayana"}
SHARED_CORE = "shared_core"


class TraditionMapper:
    def map_tradition(self, text: str, metadata: dict[str, Any] | None = None) -> str:
        metadata = metadata or {}
        explicit = str(metadata.get("tradition") or "").lower().strip()
        if explicit:
            return self._normalize(explicit)

        lowered = text.lower()
        found = {tradition for tradition in TRADITIONS if tradition in lowered}

        if found == TRADITIONS:
            return SHARED_CORE
        if len(found) == 1:
            return next(iter(found))
        if found:
            return "mixed"
        return SHARED_CORE

    def alignment_label(self, traditions: set[str]) -> str:
        normalized = {self._normalize(tradition) for tradition in traditions}
        if TRADITIONS.issubset(normalized):
            return SHARED_CORE
        if len(normalized & TRADITIONS) > 1:
            return "mixed"
        if normalized:
            return next(iter(normalized))
        return SHARED_CORE

    def _normalize(self, value: str) -> str:
        normalized = value.lower().strip().replace("-", "_").replace(" ", "_")
        if normalized == "shared":
            return SHARED_CORE
        return normalized
