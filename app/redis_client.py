import os
import redis.asyncio as redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")

r = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    decode_responses=True
)