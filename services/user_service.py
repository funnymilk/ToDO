import re
from argon2 import PasswordHasher
from fastapi import HTTPException
from models.models import User
from repository.repository import AbstractRepository
from api.dto import UserCreate as dtoUCreate, LoginData as dtoLogin
from services.exceptions import EmailExists, IncorrectName, IncorrectPassword, InputIncorrectPassword, UserNotFound

class UsersService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()
        
    def get_user(self, user_id: int):
        user = self.users_repo.get_user(user_id)
        if not user:
            raise UserNotFound
        return user
    
    def create_user(self, user: dtoUCreate):
        exists = self.users_repo.login_check(user.email)

        if exists:
            raise EmailExists    
        if user.name.strip().lower() in ["admin", "test", "user"]:
            raise IncorrectName    
        if not re.match(r"^(?=.*[A-Z])(?=.*\d).+$", user.password):
            raise IncorrectPassword
        user_data = User(
            name=user.name,
            email=user.email,
            password_hash = PasswordHasher().hash(user.password),
        )
        return self.users_repo.create_user(user_data)


    def login(self, loginData: dtoLogin):
        user = self.users_repo.login_check(loginData.email)
        
        if not user:
            raise UserNotFound
        # хэшируем введённый пароль и сравниваем bcrypt.verify(payload.password, user.password_hash)
        if not PasswordHasher().verify(user.password_hash, loginData.password):
            raise InputIncorrectPassword
        return {
            "message": "Успешный вход",
            "user_id": user.id,
            "name": user.name,
            "email": user.email
        }