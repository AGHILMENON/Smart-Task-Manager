# ===== SQLAlchemy User Service (Commented Out) =====
# from sqlalchemy.orm import Session
# from models import User
# from schemas import UserCreate
# from utils.auth import get_password_hash
#
# def get_user_by_username(db: Session, username: str):
#     return db.query(User).filter(User.username == username).first()
#
# def get_user_by_email(db: Session, email: str):
#     return db.query(User).filter(User.email == email).first()
#
# def create_user(db: Session, user: UserCreate):
#     hashed_password = get_password_hash(user.password)
#     db_user = User(
#         username=user.username,
#         email=user.email,
#         hashed_password=hashed_password
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# ===== MongoDB User Service =====
from datetime import datetime
from schemas import UserCreate
from utils.auth import get_password_hash
from typing import Optional, Dict, Any

def get_user_by_username(db, username: str) -> Optional[Dict[str, Any]]:
    \"\"\"Get user by username from MongoDB\"\"\"
    user = db.users.find_one({\"username\": username})
    return user

def get_user_by_email(db, email: str) -> Optional[Dict[str, Any]]:
    \"\"\"Get user by email from MongoDB\"\"\"
    user = db.users.find_one({\"email\": email})
    return user

def create_user(db, user: UserCreate) -> Dict[str, Any]:
    \"\"\"Create a new user in MongoDB\"\"\"
    hashed_password = get_password_hash(user.password)
    user_data = {
        \"username\": user.username,
        \"email\": user.email,
        \"hashed_password\": hashed_password,
        \"is_active\": True,
        \"created_at\": datetime.utcnow()
    }
    
    result = db.users.insert_one(user_data)
    user_data[\"_id\"] = result.inserted_id
    return user_data