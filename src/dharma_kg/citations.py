"""Citation helpers for source timestamp links."""

from __future__ import annotations

import math
from urllib.parse import urlparse

from dharma_kg.youtube import YOUTUBE_HOSTS, extract_youtube_video_id


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
