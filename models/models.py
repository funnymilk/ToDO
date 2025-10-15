from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from db.Base import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="uq_users_email"),)

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    tasks = relationship("Task", back_populates="user")  # связь «один ко многим»

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    is_done = Column(Boolean, default=False)
    deadline = Column(DateTime, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))  # связь с пользователем
    user = relationship("User", back_populates="tasks")
