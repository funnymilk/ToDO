from __future__ import annotations

import jwt
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from uuid import uuid4
from settings import Settings


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def create_access_token(*, user_id: int, settings: Settings) -> str:
    now = _utcnow()
    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.ACCESS_TTL_MINUTES)).timestamp()),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(*, user_id: int, settings: Settings) -> tuple[str, str]:
    """
    Возвращаем (refresh_token, jti)
    jti нужен, чтобы связать JWT refresh и запись в refresh_sessions.
    """
    now = _utcnow()
    jti = uuid4().hex  # уникальный id сессии
    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "type": "refresh",
        "jti": jti,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(days=settings.REFRESH_TTL_DAYS)).timestamp()),
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token, jti, payload


def decode_token(*, token: str, settings: Settings) -> Dict[str, Any]:
    """
    Важно: jwt.decode сам проверяет exp по умолчанию.
    Если токен просрочен — будет исключение ExpiredSignatureError.
    """
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
