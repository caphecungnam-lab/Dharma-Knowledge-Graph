from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from dkg_api.app.auth.auth_service import AuthError, AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginIn(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


@router.post("/login")
def login(payload: LoginIn) -> dict[str, object]:
    try:
        return AuthService().login(payload.username, payload.password)
    except AuthError as error:
        raise HTTPException(status_code=401, detail=str(error)) from error
