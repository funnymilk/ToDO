from datetime import datetime
import pytest
from repository.exceptions import ForeignKeyError, NotFound, NotUniqEmail

# ---------------------------------------------------------TASK TEST---------------------------------------------

def test_create_task(repo_task, add_user, add_task):
    task_data = {
        "title": "Test task",
        "description": "Test description",
        "is_done": False,
        "owner_id": 1,
        "deadline": datetime(2025, 12, 10, 13, 45)
    }    
    created_task = repo_task.add_one(task_data)
    assert created_task.id is not None  

def test_create_invalid_task(repo_task, add_user, add_task):
    task_data = {
        "title": "Test task",
        "description": "Test description",
        "is_done": False,
        "owner_id": 5,
        "deadline": datetime(2025, 12, 10, 13, 45)
    }    
    with pytest.raises(ForeignKeyError):
        repo_task.add_one(task_data)


def test_update_task(repo_task, add_user, add_task):
    task_data = {
        "is_done" : True,
        "deadline" : datetime(2025, 12, 10, 13, 45),
        "title" : "test",
        "description" : "ANOTHER ONE TEST"         
    }        
    updated_task = repo_task.up_task(add_task.id, task_data)
    assert updated_task.id is not None

def test_update_notExists_task(repo_task):
    task_data = {
        "is_done" : True,
        "deadline" : datetime(2025, 12, 10, 13, 45),
        "title" : "test",
        "description" : "ANOTHER ONE TEST"
    }
    with pytest.raises(NotFound):
        repo_task.up_task(12, task_data)

def test_del_exists_task(repo_task, add_user, add_task):
    repo_task.del_task(add_task.id)
    with pytest.raises(NotFound):
        repo_task.get_one(add_task.id)
    
def test_del_notExists_task(repo_task):
    with pytest.raises(NotFound):
        repo_task.del_task(1)

def test_get_all_tasks(repo_task, add_user, add_task):
    tasks = repo_task.get_all().all()
    assert len(tasks) > 0
    assert tasks[0].title == "Test task"

def test_get_isdone_tasks(repo_task, add_user, add_task):
    done_tasks = repo_task.get_isdone(False).all()
    assert all(not t.is_done for t in done_tasks)

def test_get_user_tasks_by_id(repo_task, repo_user, add_user, add_task):
    user = {
        "name" : "Don Test",
        "email" : "dontest2@exam.com",
        "password_hash" : "password"
    }     
    task_data = {
        "title": "Test task",
        "description": "Test description",
        "is_done": False,
        "owner_id": 2,
        "deadline": datetime(2025, 12, 10, 13, 45)
    }    
    repo_user.create_user(user)
    repo_task.add_one(task_data)

    tasks = repo_task.get_user_tasks(user_id=1)
    assert len(tasks) == 1
    assert tasks[0].owner_id == 1
    assert tasks[0].title == "Test task"

def test_partial_update_task(repo_task, add_user, add_task):
    data = {
        "title" : "Updated title", 
        "description" : None
    }
    ts = repo_task.get_one(add_task.id)
    updated = repo_task.up_task(add_task.id, data)
    assert updated.title == "Updated title"
    assert updated.description == None  # старое значение
    assert updated.is_done == add_task.is_done  # старое значение
    assert updated.deadline == add_task.deadline  # старое значение

def test_get_user_tasks_with_deadline(repo_task, add_user, add_task):
    deadline = datetime(2025, 12, 10, 13, 45)
    tasks = repo_task.get_user_tasks(user_id=9, deadline=deadline)
    assert len(tasks) == 1

# ---------------------------------------------------------USER TEST---------------------------------------------

def test_get_exists_User(repo_user, add_user):
    create = repo_user.get_user(add_user.id)
    assert create is not None  

def test_get_notExists_User(repo_user):
    with pytest.raises(NotFound):
        repo_user.get_user(1)

def test_success_login(repo_user, add_user):
    login_check = repo_user.login_check(add_user.email)
    assert login_check is not None  

def test_notSuccess_login(repo_user, add_user):
    with pytest.raises(NotFound):
        repo_user.login_check("sobaka@sobaka.com")

def test_success_add_user(repo_user, add_user):
    user = {
        "name" : "Don Test",
        "email" : "dontest2@exam.com",
        "password_hash" : "dontest@exam.com"
    }
    created = repo_user.create_user(user)
    assert created is not None

def test_notSuccess_add_user(repo_user, add_user):
    user = {
        "name" : "Don Test",
        "email" : "dontest@exam.com",
        "password_hash" : "dontest@exam.com"
    }
    with pytest.raises(NotUniqEmail):
        repo_user.create_user(user)
    # Убедиться, что сессия чистая 
    assert repo_user.db.query(repo_user.model).count() == 1
