from typing import Annotated
from fastapi import APIRouter, Depends, status
from api.dependencies import users_service
from schemas.schemas import LoginData, UserCreate, UserOut
from services.user_service import UsersService

router = APIRouter()

@router.get("/{user_id}", response_model=UserOut)
def get_user_endpoind(user_id: int, users_service: Annotated[UsersService, Depends(users_service)]):
    return users_service.get_user(user_id)

@router.post("/create", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user_endpoind(user: UserCreate, authService: Annotated[UsersService, Depends(users_service)]):   
    return authService.create_user(user)

@router.post("/login")
def login_endpoint(user: LoginData, authService: Annotated[UsersService, Depends(users_service)]):
    return authService.login(user)