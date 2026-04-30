# ===== SQLAlchemy Task Service (Commented Out) =====
# from sqlalchemy.orm import Session
# from models import Task
# from schemas import TaskCreate, TaskUpdate
# from typing import List
#
# def get_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100):
#     return db.query(Task).filter(Task.user_id == user_id).offset(skip).limit(limit).all()
#
# def get_task(db: Session, task_id: int, user_id: int):
#     return db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
#
# def create_task(db: Session, task: TaskCreate, user_id: int):
#     db_task = Task(**task.model_dump(), user_id=user_id)
#     db.add(db_task)
#     db.commit()
#     db.refresh(db_task)
#     return db_task
#
# def update_task(db: Session, task_id: int, task_update: TaskUpdate, user_id: int):
#     db_task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
#     if db_task:
#         update_data = task_update.model_dump(exclude_unset=True)
#         for field, value in update_data.items():
#             setattr(db_task, field, value)
#         db.commit()
#         db.refresh(db_task)
#     return db_task
#
# def delete_task(db: Session, task_id: int, user_id: int):
#     db_task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
#     if db_task:
#         db.delete(db_task)
#         db.commit()
#     return db_task

# ===== MongoDB Task Service =====
from bson import ObjectId
from models import Task
from schemas import TaskCreate, TaskUpdate
from typing import List, Optional, Dict, Any
from datetime import datetime

def get_tasks(db, user_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    \"\"\"Get all tasks for a user with pagination\"\"\"
    try:
        user_object_id = ObjectId(user_id) if isinstance(user_id, str) else user_id
    except:
        return []
    
    tasks = list(db.tasks.find({\"user_id\": user_object_id}).skip(skip).limit(limit))
    return tasks

def get_task(db, task_id: str, user_id: str) -> Optional[Dict[str, Any]]:
    \"\"\"Get a specific task by ID and verify user ownership\"\"\"
    try:
        task_object_id = ObjectId(task_id) if isinstance(task_id, str) else task_id
        user_object_id = ObjectId(user_id) if isinstance(user_id, str) else user_id
    except:
        return None
    
    task = db.tasks.find_one({\"_id\": task_object_id, \"user_id\": user_object_id})
    return task

def create_task(db, task: TaskCreate, user_id: str) -> Dict[str, Any]:
    \"\"\"Create a new task\"\"\"
    try:
        user_object_id = ObjectId(user_id) if isinstance(user_id, str) else user_id
    except:
        return None
    
    task_data = {
        \"title\": task.title,
        \"description\": task.description,
        \"completed\": False,
        \"priority\": task.priority,
        \"due_date\": task.due_date,
        \"user_id\": user_object_id,
        \"created_at\": datetime.utcnow(),
        \"updated_at\": datetime.utcnow()
    }
    
    result = db.tasks.insert_one(task_data)
    task_data[\"_id\"] = result.inserted_id
    return task_data

def update_task(db, task_id: str, task_update: TaskUpdate, user_id: str) -> Optional[Dict[str, Any]]:
    \"\"\"Update an existing task\"\"\"
    try:
        task_object_id = ObjectId(task_id) if isinstance(task_id, str) else task_id
        user_object_id = ObjectId(user_id) if isinstance(user_id, str) else user_id
    except:
        return None
    
    update_data = task_update.model_dump(exclude_unset=True)
    update_data[\"updated_at\"] = datetime.utcnow()
    
    result = db.tasks.find_one_and_update(
        {\"_id\": task_object_id, \"user_id\": user_object_id},
        {\"$set\": update_data},
        return_document=True
    )
    return result

def delete_task(db, task_id: str, user_id: str) -> Optional[Dict[str, Any]]:
    \"\"\"Delete a task\"\"\"
    try:
        task_object_id = ObjectId(task_id) if isinstance(task_id, str) else task_id
        user_object_id = ObjectId(user_id) if isinstance(user_id, str) else user_id
    except:
        return None
    
    result = db.tasks.find_one_and_delete({\"_id\": task_object_id, \"user_id\": user_object_id})
    return result