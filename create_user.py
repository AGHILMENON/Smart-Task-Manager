#!/usr/bin/env python3
import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app.database import SessionLocal, engine, Base
from models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_initial_user():
    """Create an initial admin user"""
    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == "admin").first()
        if existing_user:
            print("Admin user already exists!")
            return

        # Create admin user with hashed password (using simple hash for now)
        import hashlib
        hashed_password = hashlib.sha256("admin123".encode()).hexdigest()
        admin_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=hashed_password
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        print("✅ Initial admin user created!")
        print("Username: admin")
        print("Password: admin123")
        print("Email: admin@example.com")

    except Exception as e:
        print(f"Error creating user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_user()