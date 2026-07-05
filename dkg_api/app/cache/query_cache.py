from __future__ import annotations

import json
from collections import OrderedDict
from copy import deepcopy
from time import monotonic
from typing import Any

from dkg_api.app.db.redis_client import RedisClient


class TTLCache:
    def __init__(self, max_size: int = 512, namespace: str = "cache") -> None:
        self.max_size = max_size
        self.namespace = namespace
        self.redis = RedisClient()
        self._items: OrderedDict[str, tuple[float, Any]] = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Any | None:
        redis_value = self._redis_get(key)
        if redis_value is not None:
            self.hits += 1
            return redis_value

        entry = self._items.get(key)
        if entry is None:
            self.misses += 1
            return None

        expires_at, value = entry
        if expires_at < monotonic():
            self._items.pop(key, None)
            self.misses += 1
            return None

        self.hits += 1
        self._items.move_to_end(key)
        return deepcopy(value)

    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        self._redis_set(key, value, ttl_seconds)
        self._items[key] = (monotonic() + ttl_seconds, deepcopy(value))
        self._items.move_to_end(key)
        self._evict_if_needed()

    def stats(self) -> dict[str, object]:
        total = self.hits + self.misses
        hit_rate = self.hits / total if total else 0.0
        return {
            "size": len(self._items),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(hit_rate, 3),
        }

    def _evict_if_needed(self) -> None:
        while len(self._items) > self.max_size:
            self._items.popitem(last=False)

    def _redis_key(self, key: str) -> str:
        return f"dkg:{self.namespace}:{key}"

    def _redis_get(self, key: str) -> Any | None:
        raw = self.redis.get(self._redis_key(key))
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None

    def _redis_set(self, key: str, value: Any, ttl_seconds: int) -> None:
        try:
            self.redis.setex(
                self._redis_key(key),
                ttl_seconds,
                json.dumps(value, ensure_ascii=False),
            )
        except TypeError:
            pass


class QueryCache(TTLCache):
    def ttl_for_context(self, context: list[dict[str, Any]]) -> int:
        epistemic_types = {
            str(node.get("epistemic_type") or "") for node in context
        }
        if "interpretive" in epistemic_types or "esoteric" in epistemic_types:
            return 120
        return 900


query_cache = QueryCache(namespace="query")
