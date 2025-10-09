import re
import argon2
from fastapi import Depends, HTTPException
from requests import Session

from db.session import get_db
from models.models import User
from schemas.schemas import LoginData, UserCreate


def create_user(payload: UserCreate, db: Session = Depends(get_db)):
   # проверка дубликата email (ускоряет ошибки до коммита)
    exists = db.query(User).filter(User.email == payload.email).first()

    if payload.name.strip().lower() in ["admin", "test", "user"]:
        raise HTTPException(status_code=400, detail="Недопустимое имя пользователя")
    
    if exists:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    
    if not re.match(r"^(?=.*[A-Z])(?=.*\d).+$", payload.password):
        raise HTTPException(status_code=400, detail="Пароль должен содержать хотя бы одну цифру и заглавную букву")
    user = User(
        name=payload.name,
        email=payload.email,
        password_hash = argon2.hash(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login(payload: LoginData, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # хэшируем введённый пароль и сравниваем bcrypt.verify(payload.password, user.password_hash)
    if not argon2.verify(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Неверный пароль")

    # если всё ок — возвращаем информацию
    return {
        "message": "Успешный вход",
        "user_id": user.id,
        "name": user.name,
        "email": user.email
    }