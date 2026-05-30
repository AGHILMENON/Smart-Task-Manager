from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ===== SQLAlchemy Initialization (Commented Out) =====
# from app.database import engine, Base
# 
# # Create database tables
# Base.metadata.create_all(bind=engine)

# ===== MongoDB Connection =====
# MongoDB is initialized in app/database.py when the module is imported

from routes.auth import router as auth_router
from routes.task import router as task_router

app = FastAPI(title="Smart Task Manager", version="1.0.0")

# ===== CORS Configuration =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # React dev server
        "http://localhost:5173",    # Vite dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://localhost:8000",    # Local testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(task_router, prefix="/tasks", tags=["tasks"])

@app.get("/")
def root():
    return {"message": "Smart Task Manager API is running - MongoDB Edition"}