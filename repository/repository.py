from abc import ABC, abstractmethod
from dataclasses import asdict
from datetime import datetime, timedelta
from fastapi import Query
from db.session import SessionLocal, get_db
from api.dto import TaskCreate as dtoTCreate, TaskUpdate as dtoTUpdate
from api.dto import UserCreate as dtoUCreate
from repository.exceptions import NotFound, exceptions_trap


class AbstractRepository(ABC):
    @abstractmethod
    def add_one():
        raise NotImplementedError
    
    @abstractmethod
    def get_one():
        raise NotImplementedError
    
    @abstractmethod
    def get_all():
        raise NotImplementedError
    
    @abstractmethod
    def get_isdone():
        raise NotImplementedError
    
    @abstractmethod
    def get_user_tasks():
        raise NotImplementedError
    
    @abstractmethod
    def up_task():
        raise NotImplementedError
    
    @abstractmethod
    def del_task():
        raise NotImplementedError
    
    @abstractmethod
    def get_user():
        raise NotImplementedError
    
    @abstractmethod
    def create_user():
        raise NotImplementedError
    
    @abstractmethod
    def login_check():
        raise NotImplementedError
    
class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, db):
        self.db = db

    @exceptions_trap
    def get_one(self, task_id: int):
        task = self.db.get(self.model, task_id)
        return task
    
    def add_one(self, task: dtoTCreate):
        task_data = asdict(task)
        new_task = self.model(**task_data) 
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task
    
    @exceptions_trap
    def get_all(self):  
        task = self.db.query(self.model)
        return task
    
    @exceptions_trap
    def get_isdone(self, isdone):
        task = self.db.query(self.model).filter(self.model.is_done == isdone)
        return task
    
    @exceptions_trap
    def get_user_tasks(
        self,    
        user_id: int, 
        check: bool | None = Query(None),
        deadline: datetime | None = Query(None)
    ):        
        query = self.db.query(self.model).filter(self.model.owner_id == user_id)
        
        if query == None:
            raise NotFound
        
        if check is not None:
            query = self.db.query(self.model).filter(self.model.is_done == check)

        if deadline is not None:
            start = deadline
            end = deadline + timedelta(minutes=1)
            query = self.db.query(self.model).filter(self.model.deadline >= start, self.model.deadline < end)

        task = query.all()
        return task
    
    @exceptions_trap
    def up_task(self, task_id: int, data: dtoTUpdate):        
        task = self.db.get(self.model, task_id)
        for field, value in asdict(data).items():
            setattr(task, field, value)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    @exceptions_trap
    def del_task(self, task_id: int):
        task = self.db.get(self.model, task_id)
        if task is None:
            raise NotFound
        self.db.delete(task)
        self.db.commit()
        return task
    
    @exceptions_trap
    def get_user(self, user_id: int):
        user = self.db.get(self.model, user_id)
        return user
    
    def create_user(self, user_data: dtoUCreate):
        self.db.add(user_data)
        self.db.commit()
        self.db.refresh(user_data)
        return user_data
    
    @exceptions_trap 
    def login_check(self, email: str):
        return self.db.query(self.model).filter(self.model.email == email).first()