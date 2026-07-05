from __future__ import annotations

import re

CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def sanitize_text(value: str, max_length: int = 2000) -> str:
    sanitized = CONTROL_CHARS.sub("", value).strip()
    sanitized = re.sub(r"\s+", " ", sanitized)
    return sanitized[:max_length]
