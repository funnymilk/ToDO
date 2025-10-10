from datetime import datetime
from fastapi import HTTPException, Query, Response
from sqlalchemy.orm import Session
from repository.task_Repository import taskRepository
from schemas.schemas import TaskCreate, TaskUpdate


def create_task(payload: TaskCreate, db: Session):
    return taskRepository(db).create_task(payload)

def get_task(task_id: int, db: Session):
    task = taskRepository(db).get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="нет такой таски")
    return task

def get_alltasks(db: Session, isdone: bool | None = Query(None)):
    
    if isdone is not None:
        task = taskRepository(db).get_isdone(isdone) #НУЖЭЕН ТЕСТ, НЕ СРАБОТАЕТ ЛИ ЦЕЛДИКОМ И ПОЛНОСТЬЮ ОДНОЙ СТРОКОЙ
    else:
        task = taskRepository(db).get_alltasks()
    if not task:
        raise HTTPException(status_code=404, detail="Нет ни одной таски")
    return task

def get_user_tasks(
    user_id: int, 
    db: Session, 
    check: bool | None = Query(None),
    deadline: datetime | None = Query(None)
):    
    task = taskRepository(db).get_user_tasks(user_id, check, deadline)
    if not task:
        raise HTTPException(status_code=404, detail="Нет ни одной таски")
    return task

def up_task(task_id: int, payload: TaskUpdate, db: Session):
    task = taskRepository(db).up_task(task_id, payload)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task

def del_task(task_id: int, db: Session):
    task = taskRepository(db).del_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return Response(status_code=204)