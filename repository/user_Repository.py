from models.models import User
from repository.exceptions import exceptions_trap, trans_exceptions_trap
from repository.repository import AbstractRepositoryUser

class SQLUsersRepository(AbstractRepositoryUser):
    model = User

    def __init__(self, db):
            self.db = db
            

    @exceptions_trap
    def get_user(self, user_id: int):
        user = self.db.get(self.model, user_id)
        return user
    
    @trans_exceptions_trap
    def create_user(self, user_data: dict):
        new_user = self.model(**user_data) 
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    @exceptions_trap 
    def login_check(self, email: str):
        return self.db.query(self.model).filter(self.model.email == email).first()