from fastapi import Depends, HTTPException
from requests import Session
from db.session import get_db
from models.models import User

def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user