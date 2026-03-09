import redis.asyncio as redis
from app.redis_client import r


LIMIT = 10
WINDOW = 60


async def is_allowed(ip: str):

    key = f"rate_limit:{ip}"

    count = await r.incr(key)

    if count == 1:
        await r.expire(key, WINDOW)

    if count > LIMIT:
        return False

    return True