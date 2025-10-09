    
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from db.session import get_db
from models.models import Task, User
from schemas.schemas import TaskCreate, TaskUpdate


class userRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_user(self, user_id: int):
        user = self.db.get(User, user_id)
        return user