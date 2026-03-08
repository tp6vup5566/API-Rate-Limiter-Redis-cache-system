from fastapi import FastAPI
import redis.asyncio as redis

app = FastAPI()

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/data")
def get_data():
    return {"data": "This is some data"}

@app.get("/test-redis")
async def test_redis():
    await r.set("hello", "world")
    value = await r.get("hello")
    return {"value": value}

@app.get("/cached")
async def cached_data():
    cached = await r.get("mykey")

    if cached:
        return {"source": "cache", "data": cached}

    data = "fresh data"

    await r.set("mykey", data, ex=30)

    return {"source": "db", "data": data}