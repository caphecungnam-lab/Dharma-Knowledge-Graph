from __future__ import annotations

import os
from typing import Any


class RedisClient:
    def __init__(self) -> None:
        self.url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.client = self._client()

    def health(self) -> dict[str, object]:
        if self.client is None:
            return {"ok": False, "error": "redis package unavailable"}
        try:
            self.client.ping()
            return {"ok": True}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def get(self, key: str) -> str | None:
        if self.client is None:
            return None
        value = self.client.get(key)
        if value is None:
            return None
        if isinstance(value, bytes):
            return value.decode("utf-8")
        return str(value)

    def setex(self, key: str, ttl_seconds: int, value: str) -> None:
        if self.client is not None:
            self.client.setex(key, ttl_seconds, value)

    def incr_with_ttl(self, key: str, ttl_seconds: int) -> int:
        if self.client is None:
            return 0
        value = int(self.client.incr(key))
        if value == 1:
            self.client.expire(key, ttl_seconds)
        return value

    def _client(self) -> Any | None:
        try:
            import redis
        except Exception:
            return None
        try:
            return redis.Redis.from_url(self.url)
        except Exception:
            return None
