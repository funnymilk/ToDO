from dataclasses import asdict
from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, Query, Response, status, HTTPException
from api.dependencies import tasks_service
from schemas.schemas import TaskCreate, TaskOut, TaskUpdate, TasksToOwner
from api.dto import TaskCreate as dtoTCreate, TaskUpdate as dtoTUpdate
from services.task_service import TasksService
from api.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task_endpoind(task: TaskCreate, tasks_service: Annotated[TasksService, Depends(tasks_service)], current_user_id: Annotated[int, Depends(get_current_user)]):  
    create_data = task.model_dump()
    # enforce owner from token
    create_data["owner_id"] = current_user_id
    task_dto = dtoTCreate(**create_data)
    return tasks_service.create_task(task_dto)

@router.get("/{task_id}", response_model=TaskOut)
def get_task_endpoind(task_id: int, tasks_service: Annotated[TasksService, Depends(tasks_service)], current_user_id: Annotated[int, Depends(get_current_user)]):    
    task = tasks_service.get_task(task_id)
    # ownership check
    if task.owner_id != current_user_id:
        raise HTTPException(status_code=404, detail="Таких задач нет")
    return task

@router.get("/all/", response_model=list[TaskOut])
def get_tasks_endpoind(tasks_service: Annotated[TasksService, Depends(tasks_service)], isdone: bool | None = Query(None), current_user_id: Annotated[int, Depends(get_current_user)] = None):
    # return only tasks for current user
    return tasks_service.get_user_tasks(current_user_id, isdone, None)

@router.patch("/{task_id}/up", response_model=TaskOut)
def up_task_endpoind(task_id: int, data: TaskUpdate, tasks_service: Annotated[TasksService, Depends(tasks_service)], current_user_id: Annotated[int, Depends(get_current_user)] = None):
    # check ownership
    task = tasks_service.get_task(task_id)
    if getattr(task, "owner_id", None) != current_user_id:
        raise HTTPException(status_code=404, detail="Таких задач нет")
    update_data = data.model_dump(exclude_unset=True)
    data = dtoTUpdate(**update_data)
    update_data = {k: v for k, v in asdict(data).items() if v is not None}
    return tasks_service.up_task(task_id, update_data)

@router.delete("/{task_id}")
def del_task_endpoind(task_id: int, tasks_service: Annotated[TasksService, Depends(tasks_service)], current_user_id: Annotated[int, Depends(get_current_user)] = None):
    task = tasks_service.get_task(task_id)
    if getattr(task, "owner_id", None) != current_user_id:
        raise HTTPException(status_code=404, detail="Таких задач нет")
    tasks_service.del_task(task_id)
    return Response(status_code=204)


@router.get("/users/{user_id}", response_model=list[TasksToOwner])
def get_user_tasks_endpoint(user_id: int, tasks_service: Annotated[TasksService, Depends(tasks_service)], current_user_id: Annotated[int, Depends(get_current_user)], check: str | None = Query(None), deadline: str | None = Query(None)):
    # forbid access to other users' tasks
    if user_id != current_user_id:
        raise HTTPException(status_code=404, detail="Таких задач нет")

    isdone = None
    if check is not None:
        isdone = True if str(check).lower() == "true" else False

    deadline_dt = None
    if deadline:
        try:
            deadline_dt = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
        except Exception:
            deadline_dt = None

    return tasks_service.get_user_tasks(user_id, isdone, deadline_dt)
    

