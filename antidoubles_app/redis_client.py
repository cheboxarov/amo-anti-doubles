import redis.asyncio as aioredis
from redis.asyncio import Redis

redis: aioredis.Redis = None


async def init_redis_pool(redis_url: str):
    global redis
    redis = await aioredis.from_url(redis_url, decode_responses=True)


async def close_redis_client():
    await redis.close()
