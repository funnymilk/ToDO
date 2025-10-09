    
from datetime import datetime, timedelta
import re
import argon2
from argon2 import PasswordHasher
from fastapi import Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from db.session import get_db
from models.models import Task, User
from schemas.schemas import TaskCreate, TaskUpdate, UserCreate


class authRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, payload: UserCreate):
        user = User(
            name=payload.name,
            email=payload.email,
            password_hash = PasswordHasher().hash(payload.password),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
    
    def exists_check(self, email: str):
        exists = self.db.query(User).filter(User.email == email).first()
        return exists
    