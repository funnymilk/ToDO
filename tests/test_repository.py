from datetime import datetime
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from db.Base import Base
from repository.repository import AbstractRepository
from api.dto import TaskCreate as dtoTCreate

from repository.task_Repository import TasksRepository


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")  # in-memory база
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def repo(session: Session) -> AbstractRepository:
    
    return TasksRepository(session)

def test_create_task(repo: AbstractRepository):
    task_data = dtoTCreate(
                    title = "Test task22", 
                    description = "Test description",
                    is_done = False, 
                    owner_id = 9,
                    deadline=datetime(2025, 12, 10, 13, 45))

    created_task = repo.add_one(task_data)

    assert created_task.id is not None  
    assert created_task.title == "Test task"
    assert created_task.description == "Test description"
