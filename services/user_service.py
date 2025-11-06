import json
import re
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from repository.user_exceptions import UserNotFoundRepo
from repository.repository import AbstractRepositoryUser
from sqlalchemy.orm import Session
from api.dto import UserCreate as dtoUCreate, LoginData as dtoLogin
from services.user_exceptions import EmailExists, IncorrectName, IncorrectPassword, InputIncorrectPassword, user_exceptions_trap
from services import producer
from logger.logger import get_logger

logger = get_logger(__name__)

class UsersService:
    def __init__(self, users_repo_class: AbstractRepositoryUser, db: Session):
        self.users_repo = users_repo_class(db)
        #self.kafka_email 
    
    @user_exceptions_trap
    def get_user(self, user_id: int):
        user = self.users_repo.get_user(user_id)
        return user
    
    @user_exceptions_trap
    def create_user(self, user: dtoUCreate):
        try:
            email_exists = self.users_repo.login_check(user.email)
        except UserNotFoundRepo:
            email_exists = False
        if email_exists:
            logger.warning(f"Попытка создать пользователя с существующим email: {user.email}")
            raise EmailExists
        if user.name.strip().lower() in ["admin", "test", "user"]:
            logger.warning(f"Введено недопустимое имя: {user.email}")
            raise IncorrectName    
        if not re.match(r"^(?=.*[A-Z])(?=.*\d).+$", user.password_hash):
            logger.warning(f"ВведЁн недопустимый пароль: {user.email}")
            raise IncorrectPassword
        user_data = {
            "name"  : user.name,
            "email" : user.email,
            "password_hash" : PasswordHasher().hash(user.password_hash)
        }

        new_user = self.users_repo.create_user(user_data)   
        producer.send_task_email("user-created-topic", user_data["name"], user_data["email"])
        logger.info(f"Юзер {user_data['email']} создан")
        return new_user

    @user_exceptions_trap
    def login(self, loginData: dtoLogin):
        user = self.users_repo.login_check(loginData.email)
        # хэшируем введённый пароль и сравниваем bcrypt.verify(payload.password, user.password_hash)
        try:
            PasswordHasher().verify(user.password_hash, loginData.password)
        except VerifyMismatchError:
            raise InputIncorrectPassword
        return {
            "message": "Успешный вход",
            "user_id": user.id,
            "name": user.name,
            "email": user.email
        }