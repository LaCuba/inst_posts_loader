from app.api.schemas.auth import InstAuthModel
from app.core.redis import get_redis

from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/inst", description="Set inst auth for download posts")
async def set_inst_auth(body: InstAuthModel, rdb=Depends(get_redis)):
    await rdb.set("inst", body.model_dump_json(), ex=3600)
    return {
        "status": "ok",
    }
