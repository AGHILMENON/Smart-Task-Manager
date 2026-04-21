import os

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "devpilot_ai")

client: AsyncIOMotorClient | None = None

def get_mongo_client() -> AsyncIOMotorClient:
    global client
    if client is None:
        client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    return client


def get_database():
    return get_mongo_client()[MONGO_DB_NAME]


async def check_mongodb_connection() -> bool:
    try:
        client = get_mongo_client()
        await client.admin.command("ping")
        return True
    except ServerSelectionTimeoutError:
        return False
