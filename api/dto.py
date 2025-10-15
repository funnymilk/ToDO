from dataclasses import dataclass
from datetime import datetime


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
    password: str

@dataclass
class TaskUpdate:
    is_done: bool | None = None
    deadline: datetime | None = None
    title: str | None = None
    description: str | None = None