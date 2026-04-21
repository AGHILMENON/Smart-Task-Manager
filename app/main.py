from fastapi import FastAPI, HTTPException

from database import check_mongodb_connection
from groq_client import test_groq_connection

app = FastAPI()

@app.get("/")
def home():
    return {"message": "DevPilot AI Backend Running"}


@app.get("/db-check")
async def db_check():
    connected = await check_mongodb_connection()
    if connected:
        return {"mongodb": "connected"}
    raise HTTPException(status_code=503, detail="Cannot connect to MongoDB")


@app.get("/groq-check")
def groq_check():
    connected = test_groq_connection()
    if connected:
        return {"groq": "connected"}
    raise HTTPException(status_code=503, detail="Cannot connect to GROQ/Sanity")
