"""YouTube URL helpers."""

from __future__ import annotations

import re
from urllib.parse import parse_qs, urlparse

YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}
YOUTUBE_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")


def extract_youtube_video_id(url: str) -> str | None:
    parsed = urlparse(str(url).strip())
    host = parsed.netloc.lower()

    if host not in YOUTUBE_HOSTS:
        return None

    if host == "youtu.be":
        candidate = parsed.path.strip("/").split("/")[0]
        return candidate if YOUTUBE_ID_PATTERN.match(candidate) else None

    query_video_id = parse_qs(parsed.query).get("v", [""])[0]
    if query_video_id and YOUTUBE_ID_PATTERN.match(query_video_id):
        return query_video_id

    path_parts = [part for part in parsed.path.split("/") if part]
    if len(path_parts) >= 2 and path_parts[0] == "embed":
        candidate = path_parts[1]
        return candidate if YOUTUBE_ID_PATTERN.match(candidate) else None

    return None


def normalize_youtube_url(url: str) -> str | None:
    video_id = extract_youtube_video_id(url)
    if not video_id:
        return None
    return f"https://www.youtube.com/watch?v={video_id}"
