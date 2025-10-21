from argon2 import PasswordHasher
import pytest
from repository.exceptions import NotFound
from services.exceptions import EmailExists, IncorrectName, IncorrectPassword, InputIncorrectPassword

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