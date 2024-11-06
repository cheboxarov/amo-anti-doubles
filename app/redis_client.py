import aioredis
from aioredis import Redis

redis: Redis = None

async def init_redis_pool():
    global redis
    redis = await aioredis.from_url("redis://localhost:6379", decode_responses=True)
    print(redis)

async def close_redis_client():
    await redis.close()