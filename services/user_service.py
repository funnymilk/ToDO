import re
from argon2 import PasswordHasher
from models.models import User
from repository.exceptions import NotFound
from repository.repository import AbstractRepository
from api.dto import UserCreate as dtoUCreate, LoginData as dtoLogin
from services.exceptions import EmailExists, IncorrectName, IncorrectPassword, InputIncorrectPassword, user_exceptions_trap

class UsersService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()
    
    @user_exceptions_trap
    def get_user(self, user_id: int):
        user = self.users_repo.get_user(user_id)
        return user
    
    #@user_exceptions_trap
    def create_user(self, user: dtoUCreate):
        try:
            email_exists = self.users_repo.login_check(user.email)
        except NotFound:
            email_exists = False
   
        if email_exists:
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

    @user_exceptions_trap
    def login(self, loginData: dtoLogin):
        user = self.users_repo.login_check(loginData.email)
        # хэшируем введённый пароль и сравниваем bcrypt.verify(payload.password, user.password_hash)
        if not PasswordHasher().verify(user.password_hash, loginData.password):
            raise InputIncorrectPassword
        return {
            "message": "Успешный вход",
            "user_id": user.id,
            "name": user.name,
            "email": user.email
        }