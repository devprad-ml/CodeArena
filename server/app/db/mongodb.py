from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import settings

_client: AsyncIOMotorClient = None
_database: AsyncIOMotorDatabase = None


async def connect_to_mongo():
    """Connect to MongoDB"""
    global _client, _database
    _client = AsyncIOMotorClient(settings.MONGODB_URI)
    _database = _client[settings.MONGODB_DB_NAME]


async def close_mongo_connection():
    """Close MongoDB connection"""
    global _client
    if _client:
        _client.close()


def get_database() -> AsyncIOMotorDatabase:
    """Get MongoDB database instance"""
    return _database
