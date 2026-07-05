from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any


class AuthError(RuntimeError):
    pass


class AuthService:
    def __init__(self) -> None:
        self.secret = os.getenv("DKG_JWT_SECRET", "change-me-for-production")
        self.default_user = os.getenv("DKG_ADMIN_USER", "admin")
        self.default_password = os.getenv("DKG_ADMIN_PASSWORD", "dkg-admin")

    def login(self, username: str, password: str) -> dict[str, Any]:
        if not self._valid_credentials(username, password):
            raise AuthError("invalid_credentials")
        user = {
            "username": username,
            "role": "admin" if username == self.default_user else "viewer",
        }
        return {
            "access_token": self.generate_token(user),
            "user": {
                "role": user["role"],
            },
        }

    def generate_token(self, user: dict[str, str]) -> str:
        now = datetime.now(timezone.utc)
        header = {
            "alg": "HS256",
            "typ": "JWT",
        }
        payload = {
            "sub": user["username"],
            "role": user["role"],
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(hours=8)).timestamp()),
        }
        signing_input = ".".join(
            [
                self._b64_json(header),
                self._b64_json(payload),
            ]
        )
        signature = self._sign(signing_input)
        return f"{signing_input}.{signature}"

    def validate_token(self, token: str) -> dict[str, Any]:
        parts = token.split(".")
        if len(parts) != 3:
            raise AuthError("invalid_token")
        signing_input = ".".join(parts[:2])
        expected_signature = self._sign(signing_input)
        if not hmac.compare_digest(expected_signature, parts[2]):
            raise AuthError("invalid_token")
        payload = self._decode_json(parts[1])
        if int(payload.get("exp") or 0) < int(datetime.now(timezone.utc).timestamp()):
            raise AuthError("token_expired")
        return payload

    def _valid_credentials(self, username: str, password: str) -> bool:
        return hmac.compare_digest(username, self.default_user) and hmac.compare_digest(
            password,
            self.default_password,
        )

    def _sign(self, signing_input: str) -> str:
        digest = hmac.new(
            self.secret.encode("utf-8"),
            signing_input.encode("utf-8"),
            hashlib.sha256,
        ).digest()
        return self._b64_bytes(digest)

    def _b64_json(self, value: dict[str, Any]) -> str:
        raw = json.dumps(value, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        return self._b64_bytes(raw)

    def _decode_json(self, value: str) -> dict[str, Any]:
        padding = "=" * (-len(value) % 4)
        raw = base64.urlsafe_b64decode((value + padding).encode("utf-8"))
        return json.loads(raw.decode("utf-8"))

    def _b64_bytes(self, value: bytes) -> str:
        return base64.urlsafe_b64encode(value).decode("utf-8").rstrip("=")
