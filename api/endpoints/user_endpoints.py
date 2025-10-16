from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from api.dependencies import users_service
from schemas.schemas import LoginData, UserCreate, UserOut
from services.exceptions import EmailExists, IncorrectName, IncorrectPassword, InputIncorrectPassword, UserNotFound
from services.user_service import UsersService
from api.dto import UserCreate as dtoUCreate, LoginData as dtoLogin

router = APIRouter()

@router.get("/{user_id}", response_model=UserOut)
def get_user_endpoind(user_id: int, users_service: Annotated[UsersService, Depends(users_service)]):
    try: return users_service.get_user(user_id)
    except UserNotFound:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

@router.post("/create", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user_endpoind(user: UserCreate, authService: Annotated[UsersService, Depends(users_service)]):   
    createUserData = user.model_dump()
    data = dtoUCreate(**createUserData)
    try: return authService.create_user(data)
    except EmailExists:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    except IncorrectName:
         raise HTTPException(status_code=400, detail="Недопустимое имя пользователя")
    except IncorrectPassword:
         raise HTTPException(status_code=400, detail="Пароль должен содержать хотя бы одну цифру и заглавную букву")

@router.post("/login")
def login_endpoint(user: LoginData, authService: Annotated[UsersService, Depends(users_service)]):
    loginData = user.model_dump()
    data = dtoLogin(**loginData)
    try: 
        return authService.login(data)
    except UserNotFound:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    except InputIncorrectPassword:
        raise HTTPException(status_code=401, detail="Неверный пароль")

