from datetime import datetime, timezone, timedelta
from hashlib import sha256
from dataclasses import asdict
from typing import Annotated
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi.params import Depends
from api.jwt_utils import create_access_token, create_refresh_token, decode_token
from uuid import UUID as UUID_cls
from services.user_exceptions import InputIncorrectPassword
from services.auth_exceptions import auth_exceptions_trap, NotFoundUserForAuth, RefreshSessionNotFound
from repository.repository import AbstractRepositoryAuth, AbstractRepositoryUser
from api.dto import LoginData as dtoLogin, Token as dtoTokenRefresh, Token as dtoTokenNew
from services.user_service import UsersService
from settings import Settings, get_settings
from logger.logger import get_logger

logger = get_logger(__name__)

class AuthService:
    def __init__(self, users_service: UsersService, auth_repo: AbstractRepositoryAuth):
        # strict DI: accept ready-to-use service and auth_repo instances
        self.users_service = users_service
        self.auth_repo = auth_repo
        self.now = datetime.now(timezone.utc)

    @auth_exceptions_trap
    def authenticate(self, loginData: dtoLogin, settings: Settings):
        user = self.users_service.verify_credentials(loginData)
        

        access_token = create_access_token(user_id=user["user_id"], settings=settings)
        refresh_token, jti, payload = create_refresh_token(user_id=user["user_id"], settings=settings)
        token_new = dtoTokenNew(
            id=UUID_cls(hex=jti),
            user_id=user["user_id"],
            token_hash=sha256(refresh_token.encode("utf-8")).hexdigest(),
            created_at=self.now,
            expires_at=self.now + timedelta(minutes=settings.ACCESS_TTL_MINUTES),
            revoked_at=None,
        )
        self.auth_repo.create_session(asdict(token_new))
        logger.info("User authenticated: %s", user["user_id"])
        return {"access_token": access_token, "refresh_token": refresh_token}

    @auth_exceptions_trap
    def refresh_jti(self, refresh_token: str, settings: Settings) -> None:
        token_hash = sha256(refresh_token.encode("utf-8")).hexdigest()
        session = self.auth_repo.jti_check(token_hash)
        if not session:
            raise InputIncorrectPassword()
        user_id = decode_token(token=refresh_token, settings=settings)["sub"]

        new_access_token = create_access_token(user_id=user_id, settings=settings)
        new_refresh_token, jti, new_payload = create_refresh_token(user_id=user_id, settings=settings)

        user_data = dtoTokenRefresh(
            id=UUID_cls(hex=jti),
            user_id=int(user_id),
            token_hash=sha256(new_refresh_token.encode("utf-8")).hexdigest(),
            created_at=self.now,
            expires_at=self.now + timedelta(minutes=settings.ACCESS_TTL_MINUTES),
            revoked_at=None
        )
        self.auth_repo.refresh_jti(asdict(user_data))
        logger.info("Refresh succeeded for user: %s", user_id)
        return {"access_token": new_access_token, "refresh_token": new_refresh_token}