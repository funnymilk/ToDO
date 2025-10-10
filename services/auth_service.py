import re
from argon2 import PasswordHasher
from fastapi import HTTPException
from sqlalchemy.orm import Session

from repository.auth_Repository import authRepository
from schemas.schemas import LoginData, UserCreate


def create_user(payload: UserCreate, db: Session):
   # проверка дубликата email (ускоряет ошибки до коммита)
    exists = authRepository(db).exists_check(payload.email)

    if payload.name.strip().lower() in ["admin", "test", "user"]:
        raise HTTPException(status_code=400, detail="Недопустимое имя пользователя")    
    if exists:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")    
    if not re.match(r"^(?=.*[A-Z])(?=.*\d).+$", payload.password):
        raise HTTPException(status_code=400, detail="Пароль должен содержать хотя бы одну цифру и заглавную букву")
        
    return authRepository(db).create_user(payload)


def login(payload: LoginData, db: Session):
    
    user = authRepository(db).exists_check(payload.email)    
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    # хэшируем введённый пароль и сравниваем bcrypt.verify(payload.password, user.password_hash)
    if not PasswordHasher().verify(user.password_hash, payload.password):
        raise HTTPException(status_code=401, detail="Неверный пароль")

    # если всё ок — возвращаем информацию
    return {
        "message": "Успешный вход",
        "user_id": user.id,
        "name": user.name,
        "email": user.email
    }