    
"""from datetime import datetime, timedelta
from fastapi import Query
from sqlalchemy.orm import Session
from models.models import Task
from schemas.schemas import TaskCreate, TaskUpdate"""

from models.models import Task
from repository.repository import SQLAlchemyRepository



class TasksRepository(SQLAlchemyRepository):
    model = Task
