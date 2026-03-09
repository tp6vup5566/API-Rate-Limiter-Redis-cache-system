import time

async def token_bucket_rate_limiter(redis, key, capacity, refill_rate):

    now = time.time()

    bucket = await redis.hgetall(key)

    if bucket:
        tokens = float(bucket["tokens"])
        last_refill = float(bucket["timestamp"])
    else:
        tokens = capacity
        last_refill = now

    # calculate refill
    delta = now - last_refill
    tokens = min(capacity, tokens + delta * refill_rate)

    if tokens < 1:
        return False

    tokens -= 1

    await redis.hset(key, mapping={
        "tokens": tokens,
        "timestamp": now
    })

    return True