import redis.asyncio as redis

# Build Redis client
r = redis.Redis(host="localhost", port=6379, decode_responses=True)


async def get_cache(key: str):
    return await r.get(key)


async def set_cache(key: str, value: str, ttl: int = 30):
    await r.set(key, value, ex=ttl)