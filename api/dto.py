from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class TaskCreate:
    title: str
    description: str
    is_done: bool
    owner_id: int
    deadline: datetime | None = None    

@dataclass
class LoginData:
    email: str
    password: str

@dataclass
class UserCreate:
    name: str
    email: str
    password_hash: str

@dataclass
class TaskUpdate:
    is_done: bool | None = None
    deadline: datetime | None = None
    title: str | None = None
    description: str | None = None

@dataclass
class Token:
    id: UUID
    user_id: int
    token_hash: str
    created_at: int
    expires_at: int
    revoked_at: int | None = None