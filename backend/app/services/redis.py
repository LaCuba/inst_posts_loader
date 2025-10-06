from typing import Literal, Optional, Union
from redis.asyncio import Redis

from app.api.schemas.posts import ProcessingStatusData
from app.api.schemas.auth import InstAuthModel

RedisKey = Literal["jobs", "auth"]
RedisValue = Union[ProcessingStatusData, InstAuthModel]


class RedisManager:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def save(self, key: RedisKey, value: RedisValue, expires_in: Optional[int] = None):
        match key:
            case "jobs":
                if not isinstance(value, ProcessingStatusData):
                    raise TypeError("Unsupported model type")

                redis_key = f"jobs:{value.job_id}"
                await self.redis.set(redis_key, value.model_dump_json())
            case "auth":
                if not isinstance(value, InstAuthModel):
                    raise TypeError("Unsupported model type")

                await self.redis.set(key, value.model_dump_json(), ex=expires_in)
            case _:
                raise TypeError("Unsupported redis key")

    async def load(self, key: RedisKey, identifier: Optional[str] = None) -> RedisValue | None:
        match key:
            case 'jobs':
                redis_key = f"{key}:{identifier}"
                raw = await self.redis.get(redis_key)

                return ProcessingStatusData.model_validate_json(raw)
            case 'auth':
                raw = await self.redis.get(key)

                return InstAuthModel.model_validate_json(raw)
            case _:
                raise TypeError("Unsupported redis key")

    async def delete(self, key: RedisKey, identifier: Optional[str] = None):
        match key:
            case 'jobs':
                redis_key = f"{key}:{identifier}"
                await self.redis.delete(redis_key)
            case 'auth':
                await self.redis.delete(key)

            case _:
                raise TypeError("Unsupported redis key")
