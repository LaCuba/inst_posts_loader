from app.api.schemas.auth import InstAuthModel
from app.core.redis import get_redis

from app.services.redis import RedisManager
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/inst", description="Set inst auth for download posts")
async def set_inst_auth(body: InstAuthModel, rdb: RedisManager = Depends(get_redis)):
    await rdb.save('auth', body, 3600)
    return {
        "status": "ok",
    }
