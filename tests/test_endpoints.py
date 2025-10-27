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
    assert response.status_code == 404  
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
    assert response.status_code == 404  
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
    assert response.status_code == 404  
    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Имя не может быть одним из списка: admin, test, user"

def test_login(client, mock_users_service):
    mock_users_service.login.return_value = {
            "message": "Успешный вход",
            "user_id": 1,
            "name": "Иван",
            "email": "ivan@example.com"
        }
    url = "/users/login"
    data = {
        "email": "ivan@example.com",
        "password": "secure_password"
    }
    response = client.post(url, json=data)
    response_data = response.json()
    assert response_data["message"] == "Успешный вход"
    assert response_data["user_id"] == 1
    assert response_data["name"] == "Иван"
    assert response_data["email"] == "ivan@example.com"
    mock_users_service.login.assert_called_once()

def test_invalid_login(client, mock_users_service):
    mock_users_service.login.side_effect = UserNotFound
    url = "/users/login"
    data = {
        "email": "ivan@example.com",
        "password": "secure_password"
    }
    response = client.post(url, json=data)
    response_data = response.json()
    
    assert response.status_code == 404  
    assert "detail" in response_data
    assert response_data["detail"] == "Пользователь не найден"

def test_invalid_login(client, mock_users_service):
    mock_users_service.login.side_effect = InputIncorrectPassword
    url = "/users/login"
    data = {
        "email": "ivan@example.com",
        "password": "secure_password"
    }
    response = client.post(url, json=data)
    response_data = response.json()
    
    assert response.status_code == 404  
    assert "detail" in response_data
    assert response_data["detail"] == "Неверный пароль"

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
        "owner_id": 1,  # integer, а не строка
        "deadline": "2025-12-10 13:45"
    }
    url = "/tasks/"
    response = task_client.post(url, json=data)
    response_data = response.json()
    assert response.status_code == 201
    assert response_data["id"] == 1
    assert response_data["title"] == "str"
    mock_tasks_service.create_task.assert_called_once()

def test_invalid_tasks_create(task_client, mock_tasks_service):
    mock_tasks_service.create_task.side_effect = NotFoundUserForTask
    data = {
        "title": "str",
        "description": "str",
        "is_done": False,
        "owner_id": 2,  # integer, а не строка
        "deadline": "2025-12-10 13:45"
    }
    url = "/tasks/"
    response = task_client.post(url, json=data)
    response_data = response.json()
    assert response.status_code == 404  
    assert "detail" in response_data
    assert response_data["detail"] == "нет такого пользователя"
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
    assert response_data["detail"] == "Таких задач нет"
    mock_tasks_service.get_task.assert_called_once()

def test_getAll_tasks(task_client, mock_tasks_service):
    mock_tasks_service.get_all.return_value = [
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
    mock_tasks_service.get_all.assert_called_once_with(True)
    
    mock_tasks_service.get_all.reset_mock()
    
    response_no_param = task_client.get("/tasks/all/")
    assert response_no_param.status_code == 200
    mock_tasks_service.get_all.assert_called_once_with(None)


def test_getAll_TaskNotFound(task_client, mock_tasks_service):
    mock_tasks_service.get_all.side_effect = TaskNotFound

    response_no_param = task_client.get("/tasks/all/")
    response_data = response_no_param.json()
    
    assert response_no_param.status_code == 404
    assert "detail" in response_data
    assert response_data["detail"] == "Таких задач нет"
    mock_tasks_service.get_all.assert_called_once_with(None)
    
    mock_tasks_service.get_all.reset_mock()
    response = task_client.get("/tasks/all/", params={"isdone": "true"})
    assert response.status_code == 404
    assert "detail" in response_data
    assert response_data["detail"] == "Таких задач нет"
    mock_tasks_service.get_all.assert_called_once_with(True)


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

def test_get_user_task_TaskNotFound(task_client, mock_tasks_service):
    mock_tasks_service.get_user_tasks.side_effect = TaskNotFound

    response_no_param = task_client.get("/tasks/users/1")
    response_data = response_no_param.json()
    assert response_no_param.status_code == 404
    assert "detail" in response_data
    assert response_data["detail"] == "Таких задач нет"
    mock_tasks_service.get_user_tasks.assert_called_once_with(1, None, None)

    mock_tasks_service.get_user_tasks.reset_mock()

    response_isdone = task_client.get("/tasks/users/1", params={"check": "true"})
    response_data = response_isdone.json()
    assert response_isdone.status_code == 404
    assert "detail" in response_data
    assert response_data["detail"] == "Таких задач нет"
    mock_tasks_service.get_user_tasks.assert_called_once_with(1, True, None)

    mock_tasks_service.get_user_tasks.reset_mock()

    response_isdone_deadline = task_client.get("/tasks/users/1", params={"check": "true", "deadline": "2025-12-10 13:45"})
    response_data = response_isdone_deadline.json()
    assert response_isdone_deadline.status_code == 404
    assert "detail" in response_data
    assert response_data["detail"] == "Таких задач нет"
    mock_tasks_service.get_user_tasks.assert_called_once_with(1, True, datetime(2025, 12, 10, 13, 45))


def test_del_task(task_client, mock_tasks_service):
    mock_tasks_service.del_task.return_value = Response(status_code=204)

    response = task_client.delete("/tasks/1")
    assert response.status_code == 204

def test_del_task(task_client, mock_tasks_service):
    mock_tasks_service.del_task.side_effect = TaskNotFound

    response = task_client.delete("/tasks/1")
    response_data = response.json()
    assert response.status_code == 404
    assert "detail" in response_data
    assert response_data["detail"] == "Таких задач нет"
    mock_tasks_service.del_task.assert_called_once()