# 3) Pydantic-модели
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator

class LoginData(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title: str
    description: str
    is_done: bool
    deadline: datetime | None = None
    owner_id: int
    @field_validator("deadline", mode="before")
    def parse_deadline(cls, value): 
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d %H:%M")
            except ValueError:
                raise ValueError("Дата должна быть в формате YYYY-MM-DD HH:MM")
        return value

class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    is_done: bool
    owner_id: int
    deadline: datetime | None = None
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M")
        }

class TasksToOwner(BaseModel):
    id: int
    title: str
    description: str
    is_done: bool
    deadline: datetime | None = None
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M")
        }


class TaskUpdate(BaseModel):
    is_done: bool | None = None
    deadline: datetime | None = None
    title: str | None = None
    description: str | None = None