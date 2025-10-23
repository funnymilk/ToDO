from fastapi import Depends
from db.session import get_db
from sqlalchemy.orm import Session
from repository.task_Repository import TasksRepository
from repository.user_Repository import UsersRepository
from services.task_service import TasksService
from services.user_service import UsersService

def tasks_service(db: Session = Depends(get_db)):
    return TasksService(TasksRepository, db)

def users_service(db: Session = Depends(get_db)):
    return UsersService(UsersRepository, db)