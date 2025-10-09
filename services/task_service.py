
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Query, Response
from requests import Session
from db.session import get_db
from models.models import Task
from schemas.schemas import TaskCreate, TaskUpdate


def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = Task(
        title=payload.title,
        description=payload.description,
        owner_id=payload.owner_id,
        deadline=payload.deadline,
        is_done=payload.is_done,
        
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="нет такой таски")
    return task

def get_alltasks(db: Session = Depends(get_db), isdone: bool | None = Query(None)):
    query = db.query(Task)
    if isdone:
        query = query.filter(Task.is_done == isdone)
    elif isdone == False: query = query.filter(Task.is_done == isdone)
    task = query.all()
    if not task:
        raise HTTPException(status_code=404, detail="Нет ни одной таски")
    return task

def get_user_tasks(
    user_id: int, 
    db: Session = Depends(get_db), 
    check: bool | None = Query(None),
    deadline: datetime | None = Query(None)
):
    query = db.query(Task).filter(Task.owner_id == user_id)
    
    if check is not None:
        query = query.filter(Task.is_done == check)

    if deadline is not None:
        start = deadline
        end = deadline + timedelta(minutes=1)
        query = query.filter(Task.deadline >= start, Task.deadline < end)

    return query.all()

def up_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    data = payload.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task

def del_task(task_id: int, db: Session = Depends(get_db)):
    # 1. достаём таску
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    # 2. обновляем только то, что пришло
    db.delete(task)
    # 3. сохраняем
    db.commit()

    return Response(status_code=204)