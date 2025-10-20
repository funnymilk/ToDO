
from datetime import datetime
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from db.Base import Base
from repository.repository import AbstractRepository
from repository.task_Repository import TasksRepository
#from api.dto import TaskCreate as dtoTCreate, TaskUpdate as dtoTUpdate, UserCreate as dtoUCreate
from repository.user_Repository import UsersRepository


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")  # in-memory база
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def repo_task(session: Session) -> AbstractRepository:    
    return TasksRepository(session)

@pytest.fixture
def repo_user(session: Session) -> AbstractRepository:    
    return UsersRepository(session)

@pytest.fixture
def add_task(repo_task: AbstractRepository):
    task = {
        "title": "Test task",
        "description": "Test description",
        "is_done": False,
        "owner_id": 9,
        "deadline": datetime(2025, 12, 10, 13, 45)
    }
    return repo_task.add_one(task)

@pytest.fixture
def add_user(repo_user: AbstractRepository):
    user = {
        "name" : "Don Test",
        "email" : "dontest@exam.com",
        "password_hash" : "dontest@exam.com"
    }                    
    return repo_user.create_user(user)