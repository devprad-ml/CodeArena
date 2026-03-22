import redis.asyncio as redis

from app.config import settings

_redis_client: redis.Redis = None


async def connect_to_redis():
    """Connect to Redis"""
    global _redis_client
    _redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


async def close_redis_connection():
    """Close Redis connection"""
    global _redis_client
    if _redis_client:
        await _redis_client.close()


def get_redis() -> redis.Redis:
    """Get Redis client instance"""
    return _redis_client
