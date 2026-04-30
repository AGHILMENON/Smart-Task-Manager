from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from schemas import Task, TaskCreate, TaskUpdate
from services.task_service import (
    get_tasks, get_task, create_task, update_task, delete_task
)
from services.ai_service import suggest_task_improvements, generate_task_from_description
from .auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[Task])
def read_tasks(
    skip: int = 0, 
    limit: int = 100, 
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user_id = str(current_user["_id"])
    tasks = get_tasks(db, user_id=user_id, skip=skip, limit=limit)
    return tasks

@router.post("/", response_model=Task)
def create_new_task(
    task: TaskCreate, 
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user_id = str(current_user["_id"])
    return create_task(db, task, user_id=user_id)

@router.get("/{task_id}", response_model=Task)
def read_task(
    task_id: str, 
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user_id = str(current_user["_id"])
    db_task = get_task(db, task_id=task_id, user_id=user_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.put("/{task_id}", response_model=Task)
def update_existing_task(
    task_id: str, 
    task_update: TaskUpdate, 
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user_id = str(current_user["_id"])
    db_task = update_task(db, task_id=task_id, task_update=task_update, user_id=user_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/{task_id}")
def delete_existing_task(
    task_id: str, 
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user_id = str(current_user["_id"])
    db_task = delete_task(db, task_id=task_id, user_id=user_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

@router.post("/ai/suggest/{task_id}")
def get_task_suggestions(
    task_id: str,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user_id = str(current_user["_id"])
    db_task = get_task(db, task_id=task_id, user_id=user_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    suggestions = suggest_task_improvements(db_task["title"], db_task.get("description") or "")
    return {"task_id": task_id, "suggestions": suggestions}

@router.post("/ai/generate")
def generate_task(description: str, current_user = Depends(get_current_user)):
    result = generate_task_from_description(description)
    return {"generated_task": result}