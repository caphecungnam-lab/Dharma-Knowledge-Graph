from __future__ import annotations

import os
from collections import Counter
from time import monotonic
from typing import Callable

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from dkg_api.app.db.redis_client import RedisClient

PUBLIC_PATHS = {
    "/auth/login",
    "/health",
    "/metrics",
    "/metrics/prometheus",
}

_memory_counts: Counter[str] = Counter()
_memory_window_started = monotonic()


class ApiKeyAndRateLimitMiddleware:
    def __init__(self, app: Callable) -> None:
        self.app = app
        self.api_key = os.getenv("DKG_API_KEY", "")
        self.rate_limit = int(os.getenv("DKG_RATE_LIMIT_PER_MINUTE", "120"))
        self.redis = RedisClient()

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        if self._is_public(request.url.path):
            await self.app(scope, receive, send)
            return

        if self.api_key and request.headers.get("x-api-key") != self.api_key:
            response = JSONResponse(
                {"status": "rejected", "reason": "invalid_api_key"},
                status_code=401,
            )
            await response(scope, receive, send)
            return

        if self._rate_limited(request):
            response = JSONResponse(
                {"status": "rejected", "reason": "rate_limited"},
                status_code=429,
            )
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)

    def _is_public(self, path: str) -> bool:
        return path in PUBLIC_PATHS or path.startswith("/docs") or path.startswith("/openapi")

    def _rate_limited(self, request: Request) -> bool:
        client_host = request.client.host if request.client else "unknown"
        key = f"dkg:ratelimit:{client_host}"
        count = self.redis.incr_with_ttl(key, 60)
        if count:
            return count > self.rate_limit
        return self._memory_rate_limited(client_host)

    def _memory_rate_limited(self, client_host: str) -> bool:
        global _memory_window_started
        now = monotonic()
        if now - _memory_window_started >= 60:
            _memory_counts.clear()
            _memory_window_started = now
        _memory_counts[client_host] += 1
        return _memory_counts[client_host] > self.rate_limit
