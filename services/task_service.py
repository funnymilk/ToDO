from datetime import datetime
from fastapi import HTTPException, Query, Response
from repository.repository import AbstractRepository
from schemas.schemas import TaskCreate, TaskUpdate

class TasksService:
    def __init__(self, tasks_repo: AbstractRepository):
        self.tasks_repo: AbstractRepository = tasks_repo()

    def create_task(self, task: TaskCreate):
        task_dict = task.model_dump()
        return self.tasks_repo.add_one(task_dict)

    def get_task(self, task_id: int):
        task = self.tasks_repo.get_one(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="нет такой таски")
        return task
    
    def get_all(self, isdone: bool | None = Query(None)):
        if isdone is not None:
            task = self.tasks_repo.get_isdone(isdone) 
        else:
            task = self.tasks_repo.get_all()
        if not task:
            raise HTTPException(status_code=404, detail="Нет ни одной таски")
        return task
    
    def get_user_tasks(
        self,
        user_id: int,
        check: bool | None = Query(None),
        deadline: datetime | None = Query(None)
    ):    
        task = self.tasks_repo.get_user_tasks(user_id, check, deadline)
        if not task:
            raise HTTPException(status_code=404, detail="Нет ни одной таски")
        return task
    
    def up_task(self, task_id: int, data: TaskUpdate):
        task = self.tasks_repo.up_task(task_id, data)
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        return task
    
    def del_task(self, task_id: int):
        task = self.tasks_repo.del_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        return Response(status_code=204)