from dataclasses import asdict
from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, Query, Response, status
from api.dependencies import tasks_service
from schemas.schemas import TaskCreate, TaskOut, TaskUpdate, TasksToOwner
from api.dto import TaskCreate as dtoTCreate, TaskUpdate as dtoTUpdate
from services.task_service import TasksService

router = APIRouter()

@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task_endpoind(task: TaskCreate, tasks_service: Annotated[TasksService, Depends(tasks_service)]):  
    create_data = task.model_dump()
    task = dtoTCreate(**create_data)
    return tasks_service.create_task(task)

@router.get("/{task_id}", response_model=TaskOut)
def get_task_endpoind(task_id: int, tasks_service: Annotated[TasksService, Depends(tasks_service)]):    
        return tasks_service.get_task(task_id)

@router.get("/all/", response_model=list[TaskOut])
def get_alltasks_endpoind(tasks_service: Annotated[TasksService, Depends(tasks_service)], isdone: bool | None = Query(None)):
        return tasks_service.get_all(isdone)

@router.get("/users/{user_id}", response_model=list[TasksToOwner])
def get_user_tasks_endpoind(
    user_id: int,
    tasks_service: Annotated[TasksService, Depends(tasks_service)], 
    check: bool | None = Query(None),
    deadline: datetime | None = Query(None)
):
    return tasks_service.get_user_tasks(user_id, check, deadline)

@router.patch("/{task_id}/up", response_model=TaskOut)
def up_task_endpoind(task_id: int, data: TaskUpdate, tasks_service: Annotated[TasksService, Depends(tasks_service)]):
    update_data = data.model_dump(exclude_unset=True)
    data = dtoTUpdate(**update_data)
    update_data = {k: v for k, v in asdict(data).items() if v is not None}
    return tasks_service.up_task(task_id, update_data)

@router.delete("/{task_id}")
def del_task_endpoind(task_id: int, tasks_service: Annotated[TasksService, Depends(tasks_service)]):
    tasks_service.del_task(task_id)
    return Response(status_code=204)
    

