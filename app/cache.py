import redis.asyncio as redis
from app.redis_client import r


async def get_cache(key: str):
    return await r.get(key)


async def set_cache(key: str, value: str, ttl: int = 30):
    await r.set(key, value, ex=ttl)