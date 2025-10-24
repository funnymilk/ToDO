from datetime import datetime, timedelta
from models.models import Task
from repository.repository import AbstractRepositoryTask
from repository.task_exceptions import TaskNotFoundRepo, task_exceptions_trap
from repository.user_exceptions import UserNotFoundRepo

class SQLTasksRepository(AbstractRepositoryTask):
    model = Task

    def __init__(self, db):
            self.db = db

    @task_exceptions_trap
    def get_one(self, task_id: int):
        task = self.db.get(self.model, task_id)
        return task
    
    @task_exceptions_trap
    def add_one(self, task: dict):
        new_task = self.model(**task) 
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task
    
    @task_exceptions_trap
    def get_all(self):  
        task = self.db.query(self.model).all()
        return task
    
    @task_exceptions_trap
    def get_isdone(self, isdone):
        task = self.db.query(self.model).filter(self.model.is_done == isdone).all()
        return task
    
    @task_exceptions_trap
    def get_user_tasks(
        self,    
        user_id: int, 
        check: bool | None = None,
        deadline: datetime | None = None
    ):        
        query = self.db.query(self.model).filter(self.model.owner_id == user_id)
        
        if query == None:
            raise UserNotFoundRepo
        
        if check is not None:
            query = self.db.query(self.model).filter(self.model.is_done == check)

        if deadline is not None:
            start = deadline
            end = deadline + timedelta(minutes=1)
            query = self.db.query(self.model).filter(self.model.deadline >= start, self.model.deadline < end)

        task = query.all()
        return task
    
    @task_exceptions_trap
    def up_task(self, task_id: int, data: dict):        
        task = self.db.get(self.model, task_id)
        if task == None:
            raise TaskNotFoundRepo
        for field, value in data.items():
            setattr(task, field, value)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    @task_exceptions_trap
    def del_task(self, task_id: int):
        task = self.db.get(self.model, task_id)
        if task is None:
            raise TaskNotFoundRepo
        self.db.delete(task)
        self.db.commit()
        return task