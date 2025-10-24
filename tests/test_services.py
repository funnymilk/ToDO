from dataclasses import dataclass
from datetime import datetime
from argon2 import PasswordHasher
import pytest
from repository.exceptions import ForeignKeyError, NotFound
from services.user_exceptions import EmailExists, IncorrectName, IncorrectPassword, InputIncorrectPassword 
from services.task_exceptions import NotFoundUserForTask, TaskNotFound

# ---------------------------------------------------------USER TEST---------------------------------------------

def test_create_user_success(user_service, fake_repo):
    """Успешное создание пользователя — все проверки пройдены."""
    fake_repo.login_check.side_effect = NotFound  # email не найден

    user = type("dto", (), {
        "name": "Don",
        "email": "don@example.com",
        "password_hash": "Pass123"
    })()

    created_user = {"id": 1, "name": "Don"}
    fake_repo.create_user.return_value = created_user

    result = user_service.create_user(user)

    fake_repo.create_user.assert_called_once()
    data = fake_repo.create_user.call_args[0][0]

    # Проверяем, что пароль захэширован
    assert PasswordHasher().verify(data["password_hash"], "Pass123")
    assert result == created_user

def test_create_user_email_exists(user_service, fake_repo):
    """Если email уже существует — поднимается EmailExists."""
    fake_repo.login_check.return_value = True  # репозиторий нашёл email

    user = type("dto", (), {
        "name": "Don",
        "email": "don@example.com",
        "password_hash": "Pass123"
    })()

    with pytest.raises(EmailExists):
        user_service.create_user(user)

def test_create_user_incorrect_name(user_service, fake_repo):
    """Проверяем запрет имён admin/test/user."""
    fake_repo.login_check.side_effect = NotFound

    for bad_name in ["admin", "test", "User"]:
        user = type("dto", (), {
            "name": bad_name,
            "email": "x@example.com",
            "password_hash": "Password1"
        })()
        with pytest.raises(IncorrectName):
            user_service.create_user(user)

def test_create_user_weak_password(user_service, fake_repo):
    """Пароль без заглавной буквы или цифры — ошибка."""
    fake_repo.login_check.side_effect = NotFound

    bad_passwords = ["password", "PASSWORD", "Password", "12345"]

    for pwd in bad_passwords:
        user = type("dto", (), {
            "name": "Tom",
            "email": "tom@example.com",
            "password_hash": pwd
        })()
        with pytest.raises(IncorrectPassword):
            user_service.create_user(user)

def test_login_success(user_service, fake_repo):
    """Успешный вход — verify проходит."""
    hashed = PasswordHasher().hash("Secret123")
    fake_repo.login_check.return_value = type("User", (), {
        "id": 1,
        "name": "Tom",
        "email": "tom@example.com",
        "password_hash": hashed
    })()

    data = type("dto", (), {
        "email": "tom@example.com",
        "password": "Secret123"
    })()

    result = user_service.login(data)

    fake_repo.login_check.assert_called_once_with("tom@example.com")
    assert result["message"] == "Успешный вход"
    assert result["user_id"] == 1


def test_login_incorrect_password(user_service, fake_repo):
    """Неверный пароль — выбрасывается InputIncorrectPassword."""
    hashed = PasswordHasher().hash("CorrectPass123")

    fake_repo.login_check.return_value = type("User", (), {
        "password_hash": hashed
    })()

    data = type("dto", (), {
        "email": "test@example.com",
        "password": "WrongPassword"
    })()

    with pytest.raises(InputIncorrectPassword):
        user_service.login(data)


# ---------------------------------------------------------TASK TEST---------------------------------------------

def test_create_task(task_service, fake_repo, dto_cls_crtask, response_task):
    fake_task = dto_cls_crtask(
        title="Test task",
        description="Test description",
        is_done= False,
        owner_id= 1,
        deadline=datetime(2025, 12, 10, 13, 45)
    )

    fake_repo.add_one.return_value = response_task
    result = task_service.create_task(fake_task)

    fake_repo.add_one.assert_called_once()
    assert result == response_task

def test_creat_incorrect_task(task_service, fake_repo, dto_cls_crtask):
    fake_repo.add_one.side_effect = ForeignKeyError 
    fake_task = dto_cls_crtask(
        title="Test task",
        description="Test description",
        is_done= False,
        owner_id= 1,
        deadline=datetime(2025, 12, 10, 13, 45)
    )
    
    with pytest.raises(NotFoundUserForTask):
        task_service.create_task(fake_task)

def test_get_task(task_service, fake_repo, response_task):
    
    fake_repo.get_one.return_value = response_task
    result = task_service.get_task(response_task["task_id"])
    assert result == response_task
    fake_repo.get_one.assert_called_once()

def test_incorrect_get_task(task_service, fake_repo):
    fake_repo.get_one.side_effect = NotFound 

    with pytest.raises(TaskNotFound):
        task_service.get_task(12)

def test_get_all(task_service, fake_repo, response_tasks):
    fake_repo.get_all.return_value = response_tasks
    result = task_service.get_all()

    assert result == response_tasks
    assert len(result) == 2
    fake_repo.get_all.assert_called_once()

def test_incorrect_get_all(task_service, fake_repo):
    fake_repo.get_all.side_effect = NotFound 
    
    with pytest.raises(TaskNotFound):
        task_service.get_all()


def test_get_all_isdone(task_service, fake_repo, response_task):
    fake_repo.get_isdone.return_value = response_task

    result = task_service.get_all(False)

    assert result == response_task
    assert result["is_done"] == response_task["is_done"]
    fake_repo.get_isdone.assert_called_once()

def test_get_all_isdone_notExists(task_service, fake_repo):
    fake_repo.get_isdone.side_effect = NotFound
    is_done = ["True", "False"]

    for bl in is_done:
        with pytest.raises(TaskNotFound):
            task_service.get_all(bl)

    assert fake_repo.get_isdone.call_count == 2
    assert fake_repo.get_isdone.call_args_list[0][0][0] == "True"  # аргумент первого вызова
    assert fake_repo.get_isdone.call_args_list[1][0][0] == "False" # аргумент второго вызова



def test_get_user_tasks_exists(task_service, fake_repo, response_task):
    fake_repo.get_user_tasks.return_value = response_task
    user_id = 1
    result = task_service.get_user_tasks(user_id)
    
    assert result == response_task
    fake_repo.get_user_tasks.assert_called_once()

def test_get_user_tasks_notExists(task_service, fake_repo):
    fake_repo.get_user_tasks.side_effect = NotFound
    user_id = 1    
    
    with pytest.raises(TaskNotFound):
        task_service.get_user_tasks(user_id)
    fake_repo.get_user_tasks.assert_called_once()

def test_get_user_tasks_isdone(task_service, fake_repo, response_task):
    fake_repo.get_user_tasks.return_value = response_task
    is_done = ["True", "False"]
    user_id = 1
    
    for bl in is_done:
        result = task_service.get_user_tasks(user_id, bl)
    
    assert result == response_task
    assert fake_repo.get_user_tasks.call_count == 2
    assert fake_repo.get_user_tasks.call_args_list[0][0][1] == "True"  # аргумент первого вызова
    assert fake_repo.get_user_tasks.call_args_list[1][0][1] == "False" # аргумент второго вызова


def test_get_user_tasks_isdone_notExists(task_service, fake_repo):
    fake_repo.get_user_tasks.side_effect = NotFound
    user_id = 1    
    is_done = ["True", "False"]
    for bl in is_done:
        with pytest.raises(TaskNotFound):
            task_service.get_user_tasks(user_id, bl)
   
    assert fake_repo.get_user_tasks.call_count == 2
    assert fake_repo.get_user_tasks.call_args_list[0][0][1] == "True"  # аргумент первого вызова
    assert fake_repo.get_user_tasks.call_args_list[1][0][1] == "False" # аргумент второго вызова


def test_get_user_tasks_deadline(task_service, fake_repo, response_task):
    fake_repo.get_user_tasks.return_value = response_task
    deadline=datetime(2025, 12, 10, 13, 45)
    user_id = 1
    result = task_service.get_user_tasks(user_id, deadline)

    assert result == response_task
    fake_repo.get_user_tasks.assert_called_once()

def test_get_user_tasks_deadline_notExists(task_service, fake_repo):
    fake_repo.get_user_tasks.side_effect = NotFound
    deadline=datetime(2025, 12, 10, 13, 45)
    user_id = 1

    with pytest.raises(TaskNotFound):
        task_service.get_user_tasks(user_id, deadline)

    fake_repo.get_user_tasks.assert_called_once()

def test_task_deadline_isdone(task_service, fake_repo, response_task):
    fake_repo.get_user_tasks.return_value = response_task
    deadline=datetime(2025, 12, 10, 13, 45)
    user_id = 1
    is_done = True
    result = task_service.get_user_tasks(user_id, is_done, deadline)

    assert result == response_task
    fake_repo.get_user_tasks.assert_called_once()

def test_uptask(task_service, fake_repo, response_task, dto_cls_uptask):
    fake_repo.up_task.return_value = response_task
    fake_task = dto_cls_uptask(
        title="Test task",
        description="Test description",
        is_done= False,
        deadline=datetime(2025, 12, 10, 13, 45)
    )
    result = task_service.up_task(1, fake_task)
    assert result == response_task
    fake_repo.up_task.assert_called_once()

def test_uptask_notExists(task_service, fake_repo, dto_cls_uptask):
    fake_repo.up_task.side_effect = NotFound
    fake_task = dto_cls_uptask(
        title="Test task",
        description="Test description",
        is_done= False,
        deadline=datetime(2025, 12, 10, 13, 45)
    )
    with pytest.raises(TaskNotFound):
        task_service.up_task(1, fake_task)
    fake_repo.up_task.assert_called_once()

def test_deltask(task_service, fake_repo, response_task):
    fake_repo.del_task.return_value = response_task

    result = task_service.del_task(1)
    assert result == response_task
    fake_repo.del_task.assert_called_once()

def test_deltask_notExists(task_service, fake_repo, response_task):
    fake_repo.del_task.side_effect = NotFound

    with pytest.raises(TaskNotFound):
        task_service.del_task(1)
    fake_repo.del_task.assert_called_once()




