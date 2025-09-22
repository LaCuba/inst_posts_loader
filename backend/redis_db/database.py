import redis.asyncio as aioredis

from backend.settings import settings

redis = aioredis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)


async def get_redis():
    yield redis
