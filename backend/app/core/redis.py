from typing import AsyncGenerator
import redis.asyncio as aioredis

from app.core.settings import settings
from app.services.redis import RedisManager

redis = aioredis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)

redis_manager = RedisManager(redis)


async def get_redis() -> AsyncGenerator[RedisManager, None]:
    yield redis_manager
