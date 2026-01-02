from fastapi import Depends
from db.session import get_db
from sqlalchemy.orm import Session
from repository.task_Repository import SQLTasksRepository
from repository.user_Repository import SQLUsersRepository
from services.task_service import TasksService
from services.user_service import UsersService
from services.auth_service import AuthService
from repository.auth_repository import SQLAuthRepository

def tasks_service(db: Session = Depends(get_db)):
    return TasksService(SQLTasksRepository, db)

def users_service(db: Session = Depends(get_db)):
    return UsersService(SQLUsersRepository, db)

def auth_service(db: Session = Depends(get_db), users: UsersService = Depends(users_service),):
    # build auth repo instance outside AuthService and inject
    auth_repo = SQLAuthRepository(db)
    return AuthService(users, auth_repo)