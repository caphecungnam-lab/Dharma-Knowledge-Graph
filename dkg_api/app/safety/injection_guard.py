from __future__ import annotations

import json
import re
from collections.abc import Awaitable, Callable
from typing import Any

try:
    from starlette.requests import Request
    from starlette.responses import JSONResponse, Response
    from starlette.types import ASGIApp
except ModuleNotFoundError:
    Request = None
    JSONResponse = None
    Response = None
    ASGIApp = Any

from dkg_api.app.safety.safety_policy import critical_safety_failure


class InjectionGuard:
    BLOCK_PATTERNS = [
        r"\bignore\s+(all\s+)?previous\s+instructions\b",
        r"\bbypass\s+(the\s+)?safety\s+layer\b",
        r"\breveal\s+(the\s+)?system\s+prompt\b",
        r"\bdisable\s+validation\b",
        r"\boverride\s+(the\s+)?system\s+rules\b",
        r"\bturn\s+off\s+(the\s+)?truth\s+engine\b",
        r"\bskip\s+(the\s+)?epistemic\s+(gate|gateway|validation)\b",
        r"\bdeveloper\s+message\b.*\bignore\b",
        r"<\s*system\s*>",
        r"^\s*(system|assistant|developer)\s*:",
        r"^\s*#+\s*(instruction|system|developer)\b",
    ]

    def inspect(self, value: object) -> dict[str, object]:
        text = self._flatten(value).lower()
        for pattern in self.BLOCK_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE):
                return {
                    "status": "rejected",
                    "layer": "injection_guard",
                    "reason": "prompt_injection_detected",
                    "pattern": pattern,
                }
        return {"status": "ok", "layer": "injection_guard"}

    def assert_safe(self, value: object) -> None:
        result = self.inspect(value)
        if result["status"] != "ok":
            raise PromptInjectionBlocked(str(result["reason"]))

    def _flatten(self, value: object) -> str:
        if value is None:
            return ""
        if isinstance(value, str):
            return value
        if isinstance(value, bytes):
            try:
                return value.decode("utf-8", errors="ignore")
            except Exception:
                return ""
        if isinstance(value, dict):
            return " ".join(self._flatten(item) for item in value.values())
        if isinstance(value, list | tuple | set):
            return " ".join(self._flatten(item) for item in value)
        return str(value)


class PromptInjectionBlocked(RuntimeError):
    pass


class InjectionGuardMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app
        self.guard = InjectionGuard()

    async def __call__(self, scope: dict[str, Any], receive: Callable, send: Callable) -> None:
        if Request is None or JSONResponse is None or scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        inspection = self.guard.inspect(
            {
                "path": request.url.path,
                "query": str(request.url.query),
            }
        )
        if inspection["status"] != "ok":
            response: Response = JSONResponse(
                critical_safety_failure("injection_guard", "prompt_injection_detected"),
                status_code=400,
            )
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)
