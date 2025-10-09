from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from models.models import User
from repository.task_Repository import taskRepository
from repository.user_Repository import userRepository

def get_user(user_id: int, db: Session = Depends(get_db)):
    user = userRepository(db).get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user