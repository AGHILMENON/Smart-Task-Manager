# ===== SQLAlchemy Models (Commented Out) =====
# from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
# from sqlalchemy.sql import func
# from app.database import Base
#
# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#
# class Task(Base):
#     __tablename__ = "tasks"
#
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(Text, nullable=True)
#     completed = Column(Boolean, default=False)
#     priority = Column(String, default=\"medium\")  # low, medium, high
#     due_date = Column(DateTime, nullable=True)
#     user_id = Column(Integer, index=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# ===== MongoDB Models =====
from bson import ObjectId
from datetime import datetime
from typing import Optional

class User:
    \"\"\"MongoDB User model\"\"\"
    def __init__(self, username: str, email: str, hashed_password: str, 
                 is_active: bool = True, _id: Optional[ObjectId] = None, 
                 created_at: Optional[datetime] = None):
        self._id = _id or ObjectId()
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self):
        return {
            \"_id\": self._id,
            \"username\": self.username,
            \"email\": self.email,
            \"hashed_password\": self.hashed_password,
            \"is_active\": self.is_active,
            \"created_at\": self.created_at
        }
    
    @staticmethod
    def from_dict(data):
        return User(
            username=data.get(\"username\"),
            email=data.get(\"email\"),
            hashed_password=data.get(\"hashed_password\"),
            is_active=data.get(\"is_active\", True),
            _id=data.get(\"_id\"),
            created_at=data.get(\"created_at\")
        )

class Task:
    \"\"\"MongoDB Task model\"\"\"
    def __init__(self, title: str, user_id: ObjectId, description: Optional[str] = None,
                 completed: bool = False, priority: str = \"medium\", due_date: Optional[datetime] = None,
                 _id: Optional[ObjectId] = None, created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        self._id = _id or ObjectId()
        self.title = title
        self.description = description
        self.completed = completed
        self.priority = priority
        self.due_date = due_date
        self.user_id = user_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self):
        return {
            \"_id\": self._id,
            \"title\": self.title,
            \"description\": self.description,
            \"completed\": self.completed,
            \"priority\": self.priority,
            \"due_date\": self.due_date,
            \"user_id\": self.user_id,
            \"created_at\": self.created_at,
            \"updated_at\": self.updated_at
        }
    
    @staticmethod
    def from_dict(data):
        return Task(
            title=data.get(\"title\"),
            user_id=data.get(\"user_id\"),
            description=data.get(\"description\"),
            completed=data.get(\"completed\", False),
            priority=data.get(\"priority\", \"medium\"),
            due_date=data.get(\"due_date\"),
            _id=data.get(\"_id\"),
            created_at=data.get(\"created_at\"),
            updated_at=data.get(\"updated_at\")
        )