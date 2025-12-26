from models.models import RefreshSession
from repository.auth_exceptions import auth_exceptions_trap
from repository.repository import AbstractRepositoryAuth

class SQLAuthRepository(AbstractRepositoryAuth):
    model = RefreshSession

    def __init__(self, db):
        self.db = db

    @auth_exceptions_trap
    def create_session(self, session_data: dict):
        new_session = self.model(**session_data)
        self.db.add(new_session)
        self.db.commit()
        return new_session

    @auth_exceptions_trap
    def refresh_jti(self, new_auth: dict) -> None:
        # Revoke existing active sessions for the user, then create the new one
        from datetime import datetime
        self.db.query(self.model).filter(self.model.user_id == new_auth["user_id"], self.model.revoked_at == None).update({"revoked_at": new_auth.get("revoked_at") or datetime.utcnow()})
        new_session = self.model(user_id=new_auth["user_id"], token_hash=new_auth["token_hash"], expires_at=new_auth.get("expires_at"), revoked_at=new_auth.get("revoked_at"))
        self.db.add(new_session)
        self.db.commit()

    @auth_exceptions_trap
    def jti_check(self, jti: str):
        return self.db.query(self.model).filter(self.model.token_hash == jti, self.model.revoked_at == None).first()