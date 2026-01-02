from datetime import datetime
from fastapi import Response
import pytest
from schemas.schemas import LoginData, TaskOut, TasksToOwner, UserOut
from services.task_exceptions import NotFoundUserForTask, TaskNotFound
from services.user_exceptions import EmailExists, IncorrectName, IncorrectPassword, InputIncorrectPassword, UserNotFound

def test_get_user_success(client, mock_users_service):
    """Тест успешного получения пользователя"""    
    mock_users_service.get_user.return_value = UserOut(
        id=1,
        name="Test User",
        email="test@example.com"
    )
    # Отправляем GET запрос
    response = client.get("/users/1")    
    # Проверяем статус ответа
    assert response.status_code == 200    
    # Проверяем данные ответа
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"    
    # Проверяем, что метод get_user был вызван с правильным аргументом
    mock_users_service.get_user.assert_called_once_with(1)


def test_get_user_not_found(client, mock_users_service):
    """Тест на несуществующего пользователя"""    
    # Настраиваем мок на выброс исключения
    mock_users_service.get_user.side_effect = UserNotFound("User not found")    
    # Отправляем GET запрос
    response = client.get("/users/1")    
    # Проверяем статус ответа (зависит от вашего exception handler)
    assert response.status_code == 404    
    # Проверяем, что метод был вызван
    mock_users_service.get_user.assert_called_once_with(1)

def test_get_user_invalid_id(client):
    """Тест на некорректный ID (валидация FastAPI)"""
    
    # Отправляем запрос с некорректным ID
    response = client.get("/users/invalid")
    
    # FastAPI должен вернуть 422 (валидация не прошла)
    assert response.status_code == 422

def test_create_user(client, mock_users_service):
    mock_users_service.create_user.return_value = UserOut(
        id=1,
        name="Иван",
        email="ivan@example.com"
    )
    url = "/users/create"
    data = {
        "name": "Иван",
        "email": "ivan@example.com",
        "password_hash": "secure_password"
    }
    
    response = client.post(url, json=data)
    response_data = response.json()
    assert response.status_code == 201
    assert response_data["id"] == 1
    assert response_data["name"] == "Иван"
    mock_users_service.create_user.assert_called_once()

def test_invalidPassword_create_user(client, mock_users_service):
    mock_users_service.create_user.side_effect = IncorrectPassword
    url = "/users/create"
    data = {
        "name": "Иван",
        "email": "ivan@example.com",
        "password_hash": "secure_password"
    }    
    response = client.post(url, json=data)
    # Validation -> 422
    assert response.status_code == 422  
    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Пароль должен содержать минимум 8 символов, включая заглавную букву, цифру и специальный символ."
    
def test_invalidEmail_create_user(client, mock_users_service):
    mock_users_service.create_user.side_effect = EmailExists
    url = "/users/create"
    data = {
        "name": "Иван",
        "email": "ivan@example.com",
        "password_hash": "secure_password"
    }    
    response = client.post(url, json=data)
    # Conflict -> 409
    assert response.status_code == 409  
    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Пользователь с таким e-mail уже существует"

def test_invalidName_create_user(client, mock_users_service):
    mock_users_service.create_user.side_effect = IncorrectName
    url = "/users/create"
    data = {
        "name": "Иван",
        "email": "ivan@example.com",
        "password_hash": "secure_password"
    }    
    response = client.post(url, json=data)
    # Validation -> 422
    assert response.status_code == 422  
    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Имя не может быть одним из списка: admin, test, user"

def test_login(client, mock_users_service):
    # auth now handled by /auth/login; override auth_service dependency with a mock
    from api.dependencies import auth_service as auth_dep
    from unittest.mock import MagicMock

    mock_auth_service = MagicMock()
    mock_auth_service.authenticate.return_value = {"access_token": "at", "refresh_token": "rt"}

    # Override the auth_service dependency on the running app
    client.app.dependency_overrides[auth_dep] = lambda: mock_auth_service

    url = "/auth/login"
    data = {
        "email": "ivan@example.com",
        "password": "secure_password"
    }
    response = client.post(url, json=data)
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["access_token"] == "at"
    assert response_data["refresh_token"] == "rt"
    mock_auth_service.authenticate.assert_called_once()

    # cleanup override
    client.app.dependency_overrides.pop(auth_dep, None)

def test_invalid_login_not_found(client, mock_users_service):
    # auth endpoint used; override auth_service to raise UserNotFound
    from api.dependencies import auth_service as auth_dep
    from unittest.mock import MagicMock

    mock_auth_service = MagicMock()
    mock_auth_service.authenticate.side_effect = UserNotFound
    client.app.dependency_overrides[auth_dep] = lambda: mock_auth_service

    url = "/auth/login"
    data = {
        "email": "ivan@example.com",
        "password": "secure_password"
    }
    response = client.post(url, json=data)
    response_data = response.json()
    
    assert response.status_code == 404  
    assert "detail" in response_data
    assert response_data["detail"] == "Пользователь не найден"

    client.app.dependency_overrides.pop(auth_dep, None)

def test_invalid_login_bad_password(client, mock_users_service):
    from api.dependencies import auth_service as auth_dep
    from unittest.mock import MagicMock

    mock_auth_service = MagicMock()
    mock_auth_service.authenticate.side_effect = InputIncorrectPassword
    client.app.dependency_overrides[auth_dep] = lambda: mock_auth_service

    url = "/auth/login"
    data = {
        "email": "ivan@example.com",
        "password": "secure_password"
    }
    response = client.post(url, json=data)
    response_data = response.json()
    
    # password mismatch -> validation-like -> 422
    assert response.status_code == 422  
    assert "detail" in response_data
    assert response_data["detail"] == "Неверный пароль"

    client.app.dependency_overrides.pop(auth_dep, None)

    # ---------------------------------------------------TASKS---------------------------------------------- #
def test_tasks_create(task_client, mock_tasks_service):
    mock_tasks_service.create_task.return_value = TaskOut(
        id= 1,
        title= "str",
        description= "str",
        is_done= False,
        owner_id= 1,
        deadline= datetime(2025, 12, 10, 13, 45)
    )
    data = {
        "title": "str",
        "description": "str",
        "is_done": False,
        "deadline": "2025-12-10 13:45"
    }
    url = "/tasks/"
    response = task_client.post(url, json=data)
    response_data = response.json()
    assert response.status_code == 201
    assert response_data["id"] == 1
    assert response_data["title"] == "str"
    assert response_data["owner_id"] == 1
    mock_tasks_service.create_task.assert_called_once()

def test_invalid_tasks_create(task_client, mock_tasks_service):
    mock_tasks_service.create_task.side_effect = NotFoundUserForTask
    data = {
        "title": "str",
        "description": "str",
        "is_done": False,
        "deadline": "2025-12-10 13:45"
    }
    url = "/tasks/"
    response = task_client.post(url, json=data)
    response_data = response.json()
    assert response.status_code == 404  
    assert "detail" in response_data
    assert response_data["detail"] == "Пользователь не найден"
    mock_tasks_service.create_task.assert_called_once()

def test_get_tasks(task_client, mock_tasks_service):
    mock_tasks_service.get_task.return_value = TaskOut(
        id= 1,
        title= "str",
        description= "str",
        is_done= False,
        owner_id= 1,
        deadline= datetime(2025, 12, 10, 13, 45)
    )
    #task_id = 1
    #url = "/{task_id}"
    response = task_client.get("/tasks/1")
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["id"] == 1
    assert response_data["title"] == "str"    
    mock_tasks_service.get_task.assert_called_once()

def test_TaskNotFound_get_tasks(task_client, mock_tasks_service):
    mock_tasks_service.get_task.side_effect = TaskNotFound
    #task_id = 1
    #url = "/{task_id}"
    response = task_client.get("/tasks/1")
    response_data = response.json()
    assert response.status_code == 404
    assert "detail" in response_data
    assert response_data["detail"] == "Задача не найдена"
    mock_tasks_service.get_task.assert_called_once()


def test_get_task_not_owner(task_client, mock_tasks_service):
    # task belongs to another user
    mock_tasks_service.get_task.return_value = TaskOut(
        id=1,
        title="str",
        description="str",
        is_done=False,
        owner_id=2,
        deadline=datetime(2025, 12, 10, 13, 45)
    )
    response = task_client.get("/tasks/1")
    response_data = response.json()
    assert response.status_code == 404
    assert response_data["detail"] == "Задача не найдена"
    mock_tasks_service.get_task.assert_called_once()

def test_getAll_tasks(task_client, mock_tasks_service):
    mock_tasks_service.get_user_tasks.return_value = [
    TaskOut(id=1, title="Task 1", description="desc", is_done=True, owner_id=1, deadline=None),
    TaskOut(id=2, title="Task 2", description="desc", is_done=True, owner_id=1, deadline=None),
    ]

    # Вызываем эндпоинт с query-параметром isdone=True
    response = task_client.get("/tasks/all/", params={"isdone": "true"})
    
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[0]["is_done"] == True
    mock_tasks_service.get_user_tasks.assert_called_once_with(1, True, None)
    
    mock_tasks_service.get_user_tasks.reset_mock()
    
    response_no_param = task_client.get("/tasks/all/")
    assert response_no_param.status_code == 200
    mock_tasks_service.get_user_tasks.assert_called_once_with(1, None, None)


def test_getAll_TaskNotFound(task_client, mock_tasks_service):
    # empty result should be returned as 200 + [] (not a 404)
    mock_tasks_service.get_user_tasks.return_value = []

    response_no_param = task_client.get("/tasks/all/")
    data = response_no_param.json()
    
    assert response_no_param.status_code == 200
    assert isinstance(data, list)
    assert data == []
    mock_tasks_service.get_user_tasks.assert_called_once_with(1, None, None)
    
    mock_tasks_service.get_user_tasks.reset_mock()
    response = task_client.get("/tasks/all/", params={"isdone": "true"})
    data = response.json()
    assert response.status_code == 200
    assert data == []
    mock_tasks_service.get_user_tasks.assert_called_once_with(1, True, None)


def test_get_user_task(task_client, mock_tasks_service):
    mock_tasks_service.get_user_tasks.return_value = [
        TasksToOwner(id=1, title="Task 1", description="desc", is_done=True, deadline="2025-12-10 13:45"),
        TasksToOwner(id=2, title="Task 2", description="desc", is_done=True, deadline="2025-12-10 13:45"),
    ]

    response_no_param = task_client.get("/tasks/users/1")
    response_data = response_no_param.json()
    assert response_no_param.status_code == 200
    assert isinstance(response_data, list)
    assert len(response_data) == 2
    mock_tasks_service.get_user_tasks.assert_called_once_with(1, None, None)

    mock_tasks_service.get_user_tasks.reset_mock()

    response_isdone = task_client.get("/tasks/users/1", params={"check": "true"})
    response_data = response_isdone.json()
    assert response_isdone.status_code == 200
    assert isinstance(response_data, list)
    assert len(response_data) == 2
    mock_tasks_service.get_user_tasks.assert_called_once_with(1, True, None)

    mock_tasks_service.get_user_tasks.reset_mock()

    response_isdone_deadline = task_client.get("/tasks/users/1", params={"check": "true", "deadline": "2025-12-10 13:45"})
    response_data = response_isdone_deadline.json()
    assert response_isdone_deadline.status_code == 200
    assert isinstance(response_data, list)
    assert len(response_data) == 2
    mock_tasks_service.get_user_tasks.assert_called_once_with(1, True, datetime(2025, 12, 10, 13, 45))


def test_get_user_tasks_forbidden(task_client, mock_tasks_service):
    response = task_client.get("/tasks/users/2")
    response_data = response.json()
    assert response.status_code == 404
    assert response_data["detail"] == "Задача не найдена"

def test_get_user_task_TaskNotFound(task_client, mock_tasks_service):
    # empty result should be returned as 200 + []
    mock_tasks_service.get_user_tasks.return_value = []

    response_no_param = task_client.get("/tasks/users/1")
    data = response_no_param.json()
    assert response_no_param.status_code == 200
    assert data == []
    mock_tasks_service.get_user_tasks.assert_called_once_with(1, None, None)

    mock_tasks_service.get_user_tasks.reset_mock()

    response_isdone = task_client.get("/tasks/users/1", params={"check": "true"})
    data = response_isdone.json()
    assert response_isdone.status_code == 200
    assert data == []
    mock_tasks_service.get_user_tasks.assert_called_once_with(1, True, None)

    mock_tasks_service.get_user_tasks.reset_mock()

    response_isdone_deadline = task_client.get("/tasks/users/1", params={"check": "true", "deadline": "2025-12-10 13:45"})
    data = response_isdone_deadline.json()
    assert response_isdone_deadline.status_code == 200
    assert data == []
    mock_tasks_service.get_user_tasks.assert_called_once_with(1, True, datetime(2025, 12, 10, 13, 45))


def test_del_task_success(task_client, mock_tasks_service):
    # existing task belonging to current user
    mock_tasks_service.get_task.return_value = TaskOut(id=1, title="t", description="d", is_done=False, owner_id=1, deadline=None)
    mock_tasks_service.del_task.return_value = Response(status_code=204)

    response = task_client.delete("/tasks/1")
    assert response.status_code == 204
    mock_tasks_service.del_task.assert_called_once_with(1)


def test_del_task_not_found(task_client, mock_tasks_service):
    # task not found during delete
    mock_tasks_service.get_task.return_value = TaskOut(id=1, title="t", description="d", is_done=False, owner_id=1, deadline=None)
    mock_tasks_service.del_task.side_effect = TaskNotFound

    response = task_client.delete("/tasks/1")
    response_data = response.json()
    assert response.status_code == 404
    assert "detail" in response_data
    assert response_data["detail"] == "Задача не найдена"
    mock_tasks_service.del_task.assert_called_once_with(1)


def test_del_task_forbidden(task_client, mock_tasks_service):
    # cannot delete another user's task
    mock_tasks_service.get_task.return_value = TaskOut(id=1, title="t", description="d", is_done=False, owner_id=2, deadline=None)

    response = task_client.delete("/tasks/1")
    response_data = response.json()
    assert response.status_code == 404
    assert response_data["detail"] == "Задача не найдена"
    mock_tasks_service.del_task.assert_not_called()