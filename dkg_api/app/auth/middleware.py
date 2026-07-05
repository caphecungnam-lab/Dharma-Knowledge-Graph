from __future__ import annotations

from collections.abc import Callable

from starlette.requests import Request
from starlette.responses import JSONResponse

from dkg_api.app.auth.auth_service import AuthError, AuthService


PUBLIC_PATHS = {
    "/auth/login",
}


class JWTAuthMiddleware:
    def __init__(self, app: Callable) -> None:
        self.app = app
        self.auth = AuthService()

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        if request.method == "OPTIONS" or self._is_public(request.url.path):
            await self.app(scope, receive, send)
            return

        token = self._bearer_token(request)
        if not token:
            await self._unauthorized(scope, receive, send, "missing_token")
            return

        try:
            scope["user"] = self.auth.validate_token(token)
        except AuthError as error:
            await self._unauthorized(scope, receive, send, str(error))
            return

        await self.app(scope, receive, send)

    def _is_public(self, path: str) -> bool:
        return path in PUBLIC_PATHS

    def _bearer_token(self, request: Request) -> str | None:
        authorization = request.headers.get("authorization", "")
        prefix = "Bearer "
        if not authorization.startswith(prefix):
            return None
        return authorization[len(prefix) :].strip() or None

    async def _unauthorized(self, scope, receive, send, reason: str) -> None:
        response = JSONResponse(
            {
                "status": "rejected",
                "reason": reason,
            },
            status_code=401,
        )
        await response(scope, receive, send)
