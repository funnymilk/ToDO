    
from sqlalchemy.orm import Session
from models.models import User


class userRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int):
        user = self.db.get(User, user_id)
        return user