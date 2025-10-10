from fastapi import HTTPException
from sqlalchemy.orm import Session
from repository.user_Repository import userRepository

def get_user(user_id: int, db: Session):
    user = userRepository(db).get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user