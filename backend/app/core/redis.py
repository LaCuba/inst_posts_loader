import redis.asyncio as aioredis

from app.core.settings import settings

redis = aioredis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)


async def get_redis():
    yield redis
