from fastapi import FastAPI, HTTPException
import redis.asyncio as redis
from database import get_product_from_db
from cache import get_cache, set_cache
from limiter import is_allowed
from fastapi import Request, HTTPException
from rate_limiter import sliding_window_rate_limiter
from fastapi import Depends
from auth import verify_api_key

app = FastAPI()

r = redis.Redis(host="redis", port=6379, decode_responses=True)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/data")
async def get_data(request: Request):

    ip = request.client.host

    allowed = await is_allowed(ip)

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Too many requests"
        )

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

    await r.set(f"product:{id}", str(data), ex=60)

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