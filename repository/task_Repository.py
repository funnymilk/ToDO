    
from datetime import datetime, timedelta
from fastapi import Query
from sqlalchemy.orm import Session
from models.models import Task
from schemas.schemas import TaskCreate, TaskUpdate


class taskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, payload: TaskCreate):
        task = Task(
            title=payload.title,
            description=payload.description,
            owner_id=payload.owner_id,
            deadline=payload.deadline,
            is_done=payload.is_done,            
        )        
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def get_task(self, task_id: int):
        return self.db.get(Task, task_id)
    
    def get_alltasks(self):
        query = self.db.query(Task)        
        return query.all()
    
    def get_isdone(self, isdone):
        query = self.db.query(Task).filter(Task.is_done == isdone)
        return query.all()
    
    def get_user_tasks(
        self,    
        user_id: int, 
        check: bool | None = Query(None),
        deadline: datetime | None = Query(None)
    ):
        query = self.db.query(Task).filter(Task.owner_id == user_id)
        
        if check is not None:
            query = self.db.query(Task).filter(Task.is_done == check)

        if deadline is not None:
            start = deadline
            end = deadline + timedelta(minutes=1)
            query = self.db.query(Task).filter(Task.deadline >= start, Task.deadline < end)
        return query.all()
    
    def up_task(task_id: int, payload: TaskUpdate, self):
        task = self.db.get(Task, task_id)        
        data = payload.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(task, field, value)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def del_task(self, task_id: int):
        task = self.db.get(Task, task_id)
        self.db.delete(task)
        self.db.commit()
        return task