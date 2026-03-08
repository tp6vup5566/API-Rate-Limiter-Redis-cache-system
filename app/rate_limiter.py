import time

async def sliding_window_rate_limiter(redis, key, limit, window):
    
    now = time.time()
    window_start = now - window

    # 1. remove old requests
    await redis.zremrangebyscore(key, 0, window_start)

    # 2. count requests in window
    request_count = await redis.zcard(key)

    if request_count >= limit:
        return False

    # 3. add current request
    await redis.zadd(key, {now: now})

    # set expire so redis won't grow forever
    await redis.expire(key, window)

    return True