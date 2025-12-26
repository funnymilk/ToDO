from datetime import datetime, timedelta
import pytest


def test_create_session_and_jti_check(repo_auth):
    token_hash = "tokenhash123"
    expires_at = datetime.utcnow() + timedelta(days=7)
    sess = repo_auth.create_session({"user_id": 1, "token_hash": token_hash, "expires_at": expires_at, "revoked_at": None})

    assert sess.token_hash == token_hash
    found = repo_auth.jti_check(token_hash)
    assert found is not None
    assert found.token_hash == token_hash


def test_refresh_jti_revokes_old_and_adds_new(repo_auth):
    user_id = 1
    old_hash = "oldhash123"
    new_hash = "newhash456"

    # ensure the user exists (FK constraint)
    repo_user.create_user({"name": "User", "email": "u@example.com", "password_hash": "x"})
    repo_auth.create_session({"user_id": user_id, "token_hash": old_hash, "expires_at": datetime.utcnow() + timedelta(days=1), "revoked_at": None})

    # inspect after create
    sessions_after_create = repo_auth.db.query(repo_auth.model).all()
    print("After create ORM:", [(s.id, s.token_hash, s.revoked_at) for s in sessions_after_create])

    # rotate
    repo_auth.refresh_jti({"user_id": user_id, "token_hash": new_hash, "expires_at": datetime.utcnow() + timedelta(days=14), "revoked_at": None})

    # inspect after refresh
    sessions = repo_auth.db.query(repo_auth.model).all()
    from sqlalchemy import text
    raw = list(repo_auth.db.execute(text("SELECT id, token_hash, revoked_at FROM refresh_sessions")).all())
    print("After refresh ORM sessions:", [(s.id, s.token_hash, s.revoked_at) for s in sessions])
    print("After refresh RAW rows:", raw)

    assert any(s.token_hash == new_hash for s in sessions)
    assert any(s.token_hash == old_hash and s.revoked_at is not None for s in sessions)