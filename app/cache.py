import redis.asyncio as redis
import logging
from app.redis_client import r

logger = logging.getLogger(__name__)

async def get_cache(key: str):
    value = await r.get(key)

    if value:
        logger.info(f"Cache hit: {key}")
    else:
        logger.info(f"Cache miss: {key}")

    return value


async def set_cache(key: str, value: str, ttl: int = 30):
    await r.set(key, value, ex=ttl)