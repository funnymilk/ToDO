from datetime import datetime
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.schemas import TaskCreate, TaskOut, TaskUpdate, TasksToOwner
from services.task_service import create_task, del_task, get_alltasks, get_task, get_user_tasks, up_task

router = APIRouter()

@router.post("/tasks/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task_endpoind(task: TaskCreate, db: Session = Depends(get_db)):    
    return create_task(task, db)

@router.get("/tasks/{task_id}", response_model=TaskOut)
def get_task_endpoind(task_id: int, db: Session = Depends(get_db)):    
    return get_task(task_id, db)

@router.get("/alltask/", response_model=list[TaskOut])
def get_alltasks_endpoind(db: Session = Depends(get_db), isdone: bool | None = Query(None)):
    return get_alltasks(db, isdone)

#response_model=list[TasksToOwner]
@router.get("/users/{user_id}/tasks", response_model=list[TasksToOwner])
def get_user_tasks_endpoind(
    user_id: int, 
    db: Session = Depends(get_db), 
    check: bool | None = Query(None),
    deadline: datetime | None = Query(None)
):
    return get_user_tasks(user_id, db, check, deadline)

@router.post("/tasks/{task_id}/up", response_model=TaskOut)
def up_task_endpoind(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    return up_task(task_id, task, db)

@router.delete("/task/{task_id}")
def del_task_endpoind(task_id: int, db: Session = Depends(get_db)):
    return del_task(task_id, db)