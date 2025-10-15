from models.models import User
from repository.repository import SQLAlchemyRepository

class UsersRepository(SQLAlchemyRepository):
    model = User
