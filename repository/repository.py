from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from fastapi import Query
from db.session import SessionLocal
from schemas.schemas import TaskCreate, TaskUpdate


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
    
class SQLAlchemyRepository(AbstractRepository):
    model = None
    db = SessionLocal()
    
    def get_one(self, task_id: int):        
        return self.db.get(self.model, task_id)
    
    def add_one(self, task_data: TaskCreate):        
        new_task = self.model(**task_data) 
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task
    
    def get_all(self):  
        return self.db.query(self.model)
    
    def get_isdone(self, isdone):
        return self.db.query(self.model).filter(self.model.is_done == isdone)
    
    def get_user_tasks(
        self,    
        user_id: int, 
        check: bool | None = Query(None),
        deadline: datetime | None = Query(None)
    ):
        query = self.db.query(self.model).filter(self.model.owner_id == user_id)
        
        if check is not None:
            query = self.db.query(self.model).filter(self.model.is_done == check)

        if deadline is not None:
            start = deadline
            end = deadline + timedelta(minutes=1)
            query = self.db.query(self.model).filter(self.model.deadline >= start, self.model.deadline < end)
        return query.all()
    
    def up_task(self, task_id: int, payload: TaskUpdate):
        task = self.db.get(self.model, task_id)        
        data = payload.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(task, field, value)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def del_task(self, task_id: int):
        task = self.db.get(self.model, task_id)
        self.db.delete(task)
        self.db.commit()
        return task