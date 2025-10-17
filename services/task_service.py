from datetime import datetime
from fastapi import Query
from repository.repository import AbstractRepository
from api.dto import TaskCreate as dtoTCreate, TaskUpdate as dtoTUpdate
from services.exceptions import task_exceptions_trap

class TasksService:
    def __init__(self, tasks_repo: AbstractRepository):
        self.tasks_repo: AbstractRepository = tasks_repo()

    def create_task(self, task: dtoTCreate):
        return self.tasks_repo.add_one(task)

    @task_exceptions_trap
    def get_task(self, task_id: int):        
        task = self.tasks_repo.get_one(task_id)
        return task
    
    @task_exceptions_trap
    def get_all(self, isdone: bool | None = Query(None)):
        if isdone is not None:
            task = self.tasks_repo.get_isdone(isdone) 
        else:
            task = self.tasks_repo.get_all()
        return task
    
    @task_exceptions_trap
    def get_user_tasks(
        self,
        user_id: int,
        check: bool | None = Query(None),
        deadline: datetime | None = Query(None)
    ):    
        task = self.tasks_repo.get_user_tasks(user_id, check, deadline)
        return task
    
    @task_exceptions_trap
    def up_task(self, task_id: int, data: dtoTUpdate):
        task = self.tasks_repo.up_task(task_id, data)
        return task
    
    @task_exceptions_trap
    def del_task(self, task_id: int):
        task = self.tasks_repo.del_task(task_id)
        return task