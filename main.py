# main.py
from fastapi import FastAPI, Depends, HTTPException, Response, status, Query
from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy import Boolean, ForeignKey, create_engine, Column, Integer, String, UniqueConstraint, select, DateTime, update
from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship
from dotenv import load_dotenv
import os, hashlib
from datetime import datetime, timedelta
from fastapi.staticfiles import StaticFiles



# 1) Настройки / БД
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()

# 2) ORM-модель
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

Base.metadata.create_all(bind=engine)

# 3) Pydantic-модели
class LoginData(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
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

#--------------------------------------------------


# 4) DI: сессия
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 5) Утилита хеширования (простая для демо)
def hash_pwd(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

# 6) Приложение и маршруты
app = FastAPI(title="ToDo API")
app.mount("/home", StaticFiles(directory="home", html=True), name="home")

@app.post("/login")
def login(payload: LoginData, db: Session = Depends(get_db)):
    # ищем пользователя по email
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # хэшируем введённый пароль и сравниваем
    password_hash = hashlib.sha256(payload.password.encode("utf-8")).hexdigest()
    if user.password_hash != password_hash:
        raise HTTPException(status_code=401, detail="Неверный пароль")

    # если всё ок — возвращаем информацию
    return {
        "message": "Успешный вход",
        "user_id": user.id,
        "name": user.name,
        "email": user.email
    }

@app.post("/users/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    # проверка дубликата email (ускоряет ошибки до коммита)
    exists = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_pwd(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@app.post("/tasks/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = Task(
        title=payload.title,
        description=payload.description,
        owner_id=payload.owner_id,
        deadline=payload.deadline,
        is_done=payload.is_done,
        
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="нет такой таски")
    return task

@app.get("/alltask/", response_model=list[TaskOut])
def get_alltasks(db: Session = Depends(get_db), isdone: bool | None = Query(None)):
    #task = db.query(Task).all()
    print(">>> isdone =", isdone)  # отладка
    query = db.query(Task)
    if isdone:
        query = query.filter(Task.is_done == isdone)
    elif isdone == False: query = query.filter(Task.is_done == isdone)
    task = query.all()
    if not task:
        raise HTTPException(status_code=404, detail="Нет ни одной таски")
    return task

#response_model=list[TasksToOwner]
@app.get("/users/{user_id}/tasks", response_model=list[TasksToOwner])
def get_user_tasks(
    user_id: int, 
    db: Session = Depends(get_db), 
    check: bool | None = Query(None),
    deadline: datetime | None = Query(None)
):
    query = db.query(Task).filter(Task.owner_id == user_id)
    
    if check is not None:
        query = query.filter(Task.is_done == check)

    if deadline is not None:
        start = deadline
        end = deadline + timedelta(minutes=1)
        query = query.filter(Task.deadline >= start, Task.deadline < end)

    return query.all()

@app.post("/tasks/{task_id}/up", response_model=TaskOut)
def up_task(task_id: int,
            isdone: bool | None = Query(None),
            deadline: datetime | None = Query(None),
            title: str | None = Query(None),
            description: str | None = Query(None),
            db: Session = Depends(get_db)):
    # 1. достаём таску
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    # 2. обновляем только то, что пришло
    if isdone is not None:
        task.is_done = isdone
    if deadline is not None:
        task.deadline = deadline
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description

    # 3. сохраняем
    db.commit()
    db.refresh(task)

    return task

@app.delete("/task/{task_id}")
def del_task(task_id: int, db: Session = Depends(get_db)):
    # 1. достаём таску
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    # 2. обновляем только то, что пришло
    db.delete(task)
    # 3. сохраняем
    db.commit()

    return Response(status_code=204)


"""
@app.on_event("startup")
def show_routes():
    print("== Список зарегистрированных роутов ==")
    for route in app.routes:
        if hasattr(route, "methods"):
            print(route.path, route.methods)


sumary_line

"""


        

    
