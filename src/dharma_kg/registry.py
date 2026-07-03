"""Source Registry helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_registry(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_registry(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def find_source(registry: dict[str, Any], source_id: str) -> dict[str, Any] | None:
    for source in registry.get("sources", []):
        if isinstance(source, dict) and source.get("source_id") == source_id:
            return source
    return None


def update_source_raw_path(
    registry: dict[str, Any],
    source_id: str,
    raw_path: str,
) -> None:
    source = find_source(registry, source_id)
    if source is None:
        raise ValueError(f"Source not found: {source_id}")

    raw_paths = source.setdefault("raw_paths", [])
    if not isinstance(raw_paths, list):
        raise ValueError(f"raw_paths must be a list for source: {source_id}")

    if raw_path not in raw_paths:
        raw_paths.append(raw_path)
