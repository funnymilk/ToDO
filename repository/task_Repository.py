from models.models import Task
from repository.repository import SQLAlchemyRepository

class TasksRepository(SQLAlchemyRepository):
    model = Task
