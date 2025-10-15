import re
from argon2 import PasswordHasher
from fastapi import HTTPException
from models.models import User
from repository.repository import AbstractRepository
from schemas.schemas import LoginData, UserCreate

class UsersService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()
        
    def get_user(self, user_id: int):
        user = self.users_repo.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return user
    
    def create_user(self, user: UserCreate):
    # проверка дубликата email (ускоряет ошибки до коммита)
        print("AAAAAAAA ", user.email)
        exists = self.users_repo.login_check(user.email)

        if exists:
            raise HTTPException(status_code=400, detail="Email уже зарегистрирован")    
        if user.name.strip().lower() in ["admin", "test", "user"]:
            raise HTTPException(status_code=400, detail="Недопустимое имя пользователя")    
        if not re.match(r"^(?=.*[A-Z])(?=.*\d).+$", user.password):
            raise HTTPException(status_code=400, detail="Пароль должен содержать хотя бы одну цифру и заглавную букву")
        user_data = User(
            name=user.name,
            email=user.email,
            password_hash = PasswordHasher().hash(user.password),
        )
        #user_data = user_data.model_dump()
        return self.users_repo.create_user(user_data)


    def login(self, loginData: LoginData):
        user = self.users_repo.login_check(loginData.email)
        #user = authRepository(db).exists_check(payload.email)    
        
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        # хэшируем введённый пароль и сравниваем bcrypt.verify(payload.password, user.password_hash)
        if not PasswordHasher().verify(user.password_hash, loginData.password):
            raise HTTPException(status_code=401, detail="Неверный пароль")

        # если всё ок — возвращаем информацию
        return {
            "message": "Успешный вход",
            "user_id": user.id,
            "name": user.name,
            "email": user.email
        }