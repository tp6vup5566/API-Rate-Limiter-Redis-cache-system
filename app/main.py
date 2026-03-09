import os
import json
import logging
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
import redis.asyncio as redis
from app.database import get_product_from_db
from app.cache import get_cache, set_cache
from app.limiter import is_allowed
from app.rate_limiter import sliding_window_rate_limiter
from app.auth import verify_api_key
from app.redis_client import r

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

data = json.loads(cached)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):

    logger.info(f"Incoming request: {request.method} {request.url}")

    if request.url.path in ["/docs", "/openapi.json"]:
        return await call_next(request)

    ip = request.client.host

    allowed = await is_allowed(ip)

    if not allowed:
        logger.warning(f"Rate limit exceeded for IP {ip}")
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests"}
        )

    response = await call_next(request)

    logger.info(f"Response status: {response.status_code}")

    return response

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/data")
async def get_data():
    return {"data": "This is some data"}

@app.get("/test-redis")
async def test_redis():
    await r.set("hello", "world")
    value = await r.get("hello")
    return {"value": value}

@app.get("/cached")
async def cached_data():

    cached = await get_cache("mykey")

    if cached:
        return {"source": "cache", "data": cached}

    data = "fresh data"

    await set_cache("mykey", data, 30)

    return {"source": "db", "data": data}

@app.get("/product/{id}")
async def get_product(id: int):

    cached = await r.get(f"product:{id}")

    if cached:
        return {"source": "cache", "data": cached}

    # DB query
    data = await get_product_from_db(id)

    await r.set(f"product:{id}", json.dumps(data), ex=60)

    return {"source": "db", "data": data}

@app.get("/limited")
async def limited_api(
    user_id: str,
    api_key: str = Depends(verify_api_key)
):

    key = f"rate_limit:{user_id}"

    allowed = await sliding_window_rate_limiter(
        r,
        key,
        limit=5,
        window=60
    )

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Too many requests"
        )

    return {"message": "success"}