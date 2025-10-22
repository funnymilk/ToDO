
from dataclasses import dataclass
from datetime import datetime
from unittest.mock import Mock
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from db.Base import Base
from repository.repository import AbstractRepository
from repository.task_Repository import TasksRepository
from repository.user_Repository import UsersRepository
from sqlalchemy import event

from services.task_service import TasksService
from services.user_service import UsersService


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")  # in-memory база

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()
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
        "owner_id": 1,
        "deadline": datetime(2025, 12, 10, 13, 45)
    }
    return repo_task.add_one(task)

@pytest.fixture
def add_user(repo_user: AbstractRepository):
    user = {
        "name" : "Don Test",
        "email" : "dontest@exam.com",
        "password_hash" : "password"
    }                    
    return repo_user.create_user(user)

# ---------------------------------------------------SERVICES---------------------------------------------- #

@pytest.fixture
def fake_repo():
    return Mock()

@pytest.fixture
def user_service(fake_repo):
    """Сервис без реальной БД и репозитория."""
    service = UsersService.__new__(UsersService)
    service.users_repo = fake_repo
    return service

@pytest.fixture
def task_service(fake_repo):
    """Сервис без реальной БД и репозитория."""
    service = TasksService.__new__(TasksService)
    service.tasks_repo = fake_repo
    return service

@pytest.fixture
def dto_cls_crtask():
    cls = type("dto", (), {
        '__annotations__': {
            'title': str,
            'description': str,
            'is_done': bool,
            'owner_id': int,
            'deadline': datetime,
        }
    })
    return dataclass(cls)

@pytest.fixture
def response_task():
    response = {
        "task_id": 1,
        "title": "Test task",
        "description": "Test description",
        "is_done": False,
        "owner_id": 1,
        "deadline": datetime(2025, 12, 10, 13, 45)
    }   
    return response

@pytest.fixture
def response_tasks():
    return [
        {
            "task_id": 1,
            "title": "Test task 1",
            "description": "Test description 1",
            "is_done": False,
            "owner_id": 1,
            "deadline": datetime(2025, 12, 10, 13, 45)
        },
        {
            "task_id": 2,
            "title": "Test task 2",
            "description": "Test description 2",
            "is_done": True,
            "owner_id": 2,
            "deadline": datetime(2025, 12, 11, 9, 0)
        }
    ]

@pytest.fixture
def dto_cls_uptask():
    cls = type("dto", (), {
        '__annotations__': {
            'is_done': bool,
            'deadline': datetime,
            'title': str,
            'description': str,            
        }
    })
    return dataclass(cls)
