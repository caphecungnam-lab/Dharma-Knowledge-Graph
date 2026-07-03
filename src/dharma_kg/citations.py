"""Citation helpers for source timestamp links."""

from __future__ import annotations

import math
import re
from urllib.parse import parse_qs, urlparse

YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}
YOUTUBE_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")


def parse_time_to_seconds(time_str: str) -> int:
    value = str(time_str).strip()
    if not value:
        raise ValueError("Time value is empty")

    if value.isdigit():
        return int(value)

    parts = value.split(":")
    if len(parts) == 2:
        minutes = int(parts[0])
        seconds = float(parts[1])
        return math.floor((minutes * 60) + seconds)

    if len(parts) == 3:
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])
        return math.floor((hours * 3600) + (minutes * 60) + seconds)

    raise ValueError(f"Invalid time value: {time_str}")


def is_youtube_url(url: str) -> bool:
    parsed = urlparse(str(url).strip())
    return parsed.netloc.lower() in YOUTUBE_HOSTS


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


def build_youtube_timestamp_url(source_url: str, start_time: str) -> str | None:
    video_id = extract_youtube_video_id(source_url)
    if not video_id:
        return None

    try:
        seconds = parse_time_to_seconds(start_time)
    except (TypeError, ValueError):
        return None

    return f"https://www.youtube.com/watch?v={video_id}&t={seconds}s"


def build_citation_label(
    video_id: str | None,
    start_time: str,
    end_time: str,
) -> str:
    time_range = " -> ".join(value for value in [start_time, end_time] if value)
    parts = [part for part in [video_id, time_range] if part]
    return " | ".join(parts)
