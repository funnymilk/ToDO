from datetime import datetime, timedelta
from argon2 import PasswordHasher
from hashlib import sha256
import pytest

from api.dto import LoginData as dtoLogin
from services.auth_service import AuthService
from repository.user_Repository import SQLUsersRepository
from repository.auth_repository import SQLAuthRepository
from services.user_service import UsersService
from services.user_exceptions import InputIncorrectPassword


def test_authenticate_stores_session(session, repo_user, repo_auth):
    # create user with hashed password
    pwd = "Secret123"
    hashed = PasswordHasher().hash(pwd)
    user = repo_user.create_user({"name": "Tom", "email": "tom@example.com", "password_hash": hashed})

    # build dependencies explicitly for AuthService
    users_service = UsersService(SQLUsersRepository, session)
    auth_repo = SQLAuthRepository(session)
    auth_service = AuthService(users_service, auth_repo)

    res = auth_service.authenticate(dtoLogin(email="tom@example.com", password=pwd), settings=__import__('settings').get_settings())

    assert "access_token" in res and "refresh_token" in res

    token_hash = sha256(res["refresh_token"].encode("utf-8")).hexdigest()
    # verify DB directly (avoid repo wrapper which raises)
    found = repo_auth.db.query(repo_auth.model).filter(repo_auth.model.token_hash == token_hash, repo_auth.model.revoked_at == None).first()
    assert found is not None


def test_authenticate_incorrect_password(session, repo_user):
    pwd = "GoodPass1"
    hashed = PasswordHasher().hash(pwd)
    repo_user.create_user({"name": "Tom", "email": "tom2@example.com", "password_hash": hashed})

    users_service = UsersService(SQLUsersRepository, session)
    auth_repo = SQLAuthRepository(session)
    auth_service = AuthService(users_service, auth_repo)

    with pytest.raises(InputIncorrectPassword):
        auth_service.authenticate(dtoLogin(email="tom2@example.com", password="BadPass"), settings=__import__('settings').get_settings())


def test_refresh_rotates_tokens(session, repo_user, repo_auth):
    pwd = "SecretX1"
    hashed = PasswordHasher().hash(pwd)
    repo_user.create_user({"name": "Sam", "email": "sam@example.com", "password_hash": hashed})

    users_service = UsersService(SQLUsersRepository, session)
    auth_repo = SQLAuthRepository(session)
    auth_service = AuthService(users_service, auth_repo)

    res = auth_service.authenticate(dtoLogin(email="sam@example.com", password=pwd), settings=__import__('settings').get_settings())
    old_refresh = res["refresh_token"]
    old_hash = sha256(old_refresh.encode("utf-8")).hexdigest()

    new_res = auth_service.refresh_jti(old_refresh, settings=__import__('settings').get_settings())
    assert "access_token" in new_res and "refresh_token" in new_res

    # old token should be revoked
    assert repo_auth.jti_check(old_hash) is None
    new_hash = sha256(new_res["refresh_token"].encode("utf-8")).hexdigest()
    assert repo_auth.jti_check(new_hash) is not None