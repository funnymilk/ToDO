from datetime import datetime
import pytest
from repository.exceptions import NotFound
from repository.repository import AbstractRepository
from api.dto import TaskCreate as dtoTCreate, TaskUpdate as dtoTUpdate, UserCreate as dtoUCreate

# ---------------------------------------------------------TASK TEST---------------------------------------------

def test_create_task(repo_task: AbstractRepository, add_task):
    task_data = dtoTCreate(
                    title = "Test task", 
                    description = "Test description",
                    is_done = False, 
                    owner_id = 9,
                    deadline = datetime(2025, 12, 10, 13, 45))
    created_task = repo_task.add_one(task_data)
    assert created_task.id is not None  

def test_update_task(repo_task: AbstractRepository, add_task):
    task_data = dtoTUpdate(
                    is_done = True,
                    deadline = datetime(2025, 12, 10, 13, 45),
                    title = "test",
                    description = "ANOTHER ONE TEST")
    
    updated_task = repo_task.up_task(add_task.id, task_data)
    assert updated_task.id is not None

def test_update_notExists_task(repo_task: AbstractRepository):
    task_data = dtoTUpdate(
                    is_done = True,
                    deadline = datetime(2025, 12, 10, 13, 45),
                    title = "test",
                    description = "ANOTHER ONE TEST")

    with pytest.raises(NotFound) as exc_info:
        repo_task.up_task(12, task_data)
    assert isinstance(exc_info.value, NotFound)

def test_del_exists_task(repo_task: AbstractRepository, add_task):
    del_task = repo_task.del_task(add_task.id)
    assert del_task.id is not None  
    
def test_del_notExists_task(repo_task: AbstractRepository):
    with pytest.raises(NotFound) as exc_info:
        repo_task.del_task(1)
    assert isinstance(exc_info.value, NotFound)

# ---------------------------------------------------------USER TEST---------------------------------------------

def test_get_exists_User(repo_user: AbstractRepository, add_user):
    create = repo_user.get_user(add_user.id)
    assert create is not None  

def test_get_notExists_User(repo_user: AbstractRepository):
    with pytest.raises(NotFound) as exc_info:
        repo_user.get_user(1)
    assert isinstance(exc_info.value, NotFound)

def test_success_login(repo_user: AbstractRepository, add_user):
    login_check = repo_user.login_check(add_user.email)
    assert login_check is not None  

def test_notSuccess_login(repo_user: AbstractRepository, add_user):
    with pytest.raises(NotFound) as exc_info:
        repo_user.login_check("sobaka@sobaka.com")
    assert isinstance(exc_info.value, NotFound)

def test_success_add_user(repo_user: AbstractRepository, add_user):
    user = dtoUCreate(
                    name = "Don Test",
                    email = "dontest@exam.com",
                    password_hash = "dontest@exam.com")   
    created = repo_user.create_user(user)
    assert created is not None

# как првоерить создание юзера, в случае если он вернул None? Такое возможно вообще?