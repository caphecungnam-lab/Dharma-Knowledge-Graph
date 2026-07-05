from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

REQUIRED_METADATA_FIELDS = {"source_id", "tradition", "author", "title"}
SUPPORTED_TRADITIONS = {"theravada", "mahayana", "vajrayana", "unknown"}


class CorpusLoader:
    def load(
        self,
        file_path: str | Path,
        source_metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        path = Path(file_path)
        metadata = self._metadata(path, source_metadata or {})
        text = self._load_text(path)
        return {
            "text": self._clean_text(text),
            "source_metadata": metadata,
        }

    def _load_text(self, path: Path) -> str:
        suffix = path.suffix.lower()
        if suffix == ".txt":
            return path.read_text(encoding="utf-8")
        if suffix == ".json":
            payload = json.loads(path.read_text(encoding="utf-8"))
            return str(payload.get("text") or payload.get("transcript") or "")
        if suffix == ".pdf":
            return self._load_pdf(path)
        raise ValueError(f"Unsupported corpus file type: {suffix}")

    def _load_pdf(self, path: Path) -> str:
        try:
            from pypdf import PdfReader
        except Exception as error:
            raise RuntimeError("PDF ingestion requires pypdf.") from error

        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    def _metadata(
        self,
        path: Path,
        source_metadata: dict[str, Any],
    ) -> dict[str, Any]:
        metadata = {
            "source_id": source_metadata.get("source_id") or path.stem,
            "tradition": source_metadata.get("tradition") or "unknown",
            "author": source_metadata.get("author"),
            "title": source_metadata.get("title") or path.stem,
            "source_type": source_metadata.get("source_type") or self._source_type(path),
        }
        missing = REQUIRED_METADATA_FIELDS - metadata.keys()
        if missing:
            raise ValueError(f"Missing source metadata fields: {sorted(missing)}")
        if metadata["tradition"] not in SUPPORTED_TRADITIONS:
            raise ValueError(f"Unsupported tradition: {metadata['tradition']}")
        return metadata

    def _source_type(self, path: Path) -> str:
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            return "pdf"
        if suffix == ".txt":
            return "text"
        if suffix == ".json":
            return "transcript"
        return "unknown"

    def _clean_text(self, text: str) -> str:
        text = text.replace("\ufeff", " ")
        text = re.sub(r"\s+", " ", text)
        return text.strip()
