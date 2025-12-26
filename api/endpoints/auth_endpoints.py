from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from api.dependencies import auth_service
from services.auth_service import AuthService
from settings import get_settings, Settings
from schemas.schemas import LoginRequest, TokenResponse
from api.dto import LoginData as dtoLogin
from logger.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    auth_service: Annotated[AuthService, Depends(auth_service)],
    settings: Annotated[Settings, Depends(get_settings)]
):
    """Authenticate user and return (access_token, refresh_token)."""
    loginData = data.model_dump()
    data = dtoLogin(**loginData)  
    logger.info(f"Попытка входа пользователя: {data.email}")

    return auth_service.authenticate(data, settings)

@router.post("/refresh", response_model=TokenResponse)
def refresh(
    refresh_token: str,
    auth_service: Annotated[AuthService, Depends(auth_service)],
    settings: Annotated[Settings, Depends(get_settings)]
):
    """Refresh access and refresh tokens using a valid refresh token."""
    return auth_service.refresh_jti(refresh_token, settings)