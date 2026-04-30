# ===== SQLite Configuration (Commented Out) =====
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
#
# SQLALCHEMY_DATABASE_URL = "sqlite:///./smart_task_manager.db"
#
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# ===== MongoDB Configuration =====
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from app.config import MONGODB_URL, DATABASE_NAME

try:
    client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
    # Verify connection
    client.admin.command('ping')
    db = client[DATABASE_NAME]
    
    # Create collections with validation
    if "users" not in db.list_collection_names():
        db.create_collection("users")
        db["users"].create_index("username", unique=True)
        db["users"].create_index("email", unique=True)
    
    if "tasks" not in db.list_collection_names():
        db.create_collection("tasks")
        db["tasks"].create_index("user_id")
        db["tasks"].create_index("created_at")
    
    print(f"Connected to MongoDB at {MONGODB_URL}")
    print(f"Database: {DATABASE_NAME}")
except ServerSelectionTimeoutError as e:
    print(f"Failed to connect to MongoDB: {e}")
    print(f"Make sure MongoDB is running at {MONGODB_URL}")
    raise

def get_db():
    """Get MongoDB database instance"""
    return db

# SQLAlchemy compatibility (commented out)
# Base = None
