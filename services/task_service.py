from dataclasses import asdict
from datetime import datetime
from repository.repository import AbstractRepositoryTask
from api.dto import TaskCreate as dtoTCreate, TaskUpdate as dtoTUpdate
from sqlalchemy.orm import Session
from services.task_exceptions import task_exceptions_trap
from logger.logger import get_logger

logger = get_logger(__name__)

class TasksService:
    def __init__(self, tasks_repo_class: AbstractRepositoryTask, db: Session):
        self.tasks_repo = tasks_repo_class(db)
    
    @task_exceptions_trap
    def create_task(self, task: dtoTCreate):
        # 1. проверить что юзер активный
        # 2. то тогда создаём таск
        # 3. в противном случае ошибка "юзер не активный"
        # 4. открываешь транзацкцию и проверяешь юзера
        new_task = self.tasks_repo.add_one(asdict(task))
        logger.info("Task created: %s", getattr(new_task, 'id', new_task))
        return new_task

    @task_exceptions_trap
    def get_task(self, task_id: int):        
        task = self.tasks_repo.get_one(task_id)
        return task
    
    @task_exceptions_trap
    def get_all(self, isdone: bool | None = None):
        if isdone is not None:
            return self.tasks_repo.get_isdone(isdone) 
        return self.tasks_repo.get_all()
    
    @task_exceptions_trap
    def get_user_tasks(
        self,
        user_id: int,
        check: bool | None = None,
        deadline: datetime | None = None
    ):    
        task = self.tasks_repo.get_user_tasks(user_id, check, deadline)
        return task
    
    @task_exceptions_trap
    def up_task(self, task_id: int, task: dtoTUpdate):
        return self.tasks_repo.up_task(task_id, task)
    
    @task_exceptions_trap
    def del_task(self, task_id: int):
        task = self.tasks_repo.del_task(task_id)
        logger.info("Task deleted: %s", task_id)
        return task