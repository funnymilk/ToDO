from dataclasses import asdict
from datetime import datetime
from fastapi import Query
from repository.repository import AbstractRepository
from api.dto import TaskCreate as dtoTCreate, TaskUpdate as dtoTUpdate
from sqlalchemy.orm import Session

from services.exceptions import exceptions_trap

class TasksService:
    def __init__(self, tasks_repo_class: AbstractRepository, db: Session):
        self.tasks_repo = tasks_repo_class(db)

    @exceptions_trap
    def create_task(self, task: dtoTCreate):
        task_data = {k: v for k, v in asdict(task).items() if v is not None}
        return self.tasks_repo.add_one(task_data)

    @exceptions_trap
    def get_task(self, task_id: int):        
        task = self.tasks_repo.get_one(task_id)
        return task
    
    @exceptions_trap
    def get_all(self, isdone: bool | None = None):
        if isdone is not None:
            task = self.tasks_repo.get_isdone(isdone) 
        else:
            task = self.tasks_repo.get_all()
        return task
    
    @exceptions_trap
    def get_user_tasks(
        self,
        user_id: int,
        check: bool | None = None,
        deadline: datetime | None = None
    ):    
        task = self.tasks_repo.get_user_tasks(user_id, check, deadline)
        return task
    
    @exceptions_trap
    def up_task(self, task_id: int, task: dtoTUpdate):
        update_data = {k: v for k, v in asdict(task).items() if v is not None}
        return self.tasks_repo.up_task(task_id, update_data)
    
    @exceptions_trap
    def del_task(self, task_id: int):
        task = self.tasks_repo.del_task(task_id)
        return task