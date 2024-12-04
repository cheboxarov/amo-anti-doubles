import redis.asyncio as aioredis
from redis.asyncio import Redis
from config import REDIS_URL

redis: aioredis.Redis = None


async def init_redis_pool():
    global redis
    redis = await aioredis.from_url(REDIS_URL, decode_responses=True)
    await redis.flushall()
    await redis.flushdb()


async def close_redis_client():
    await redis.close()
