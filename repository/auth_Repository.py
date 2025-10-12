    
from argon2 import PasswordHasher
from sqlalchemy.orm import Session
from models.models import User
from schemas.schemas import UserCreate


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
    