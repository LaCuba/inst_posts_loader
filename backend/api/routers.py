from backend.api.models import InstaAuthModel, DownloadModel
from backend.api.controllers import download_posts

from sqlalchemy import select
from backend.db.database import get_session
from backend.db.models import Account
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/ping")
def root():
    return {"message": "pong!"}


@router.post("/set_insta_auth", description="Set insta auth for download posts")
def set_insta_auth(body: InstaAuthModel):
    # Keep auth data in redis
    return {
        "status": "ok",
    }


@router.get("/accounts")
async def list_accounts(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Account))
    return result.scalars().all()


@router.get("/accounts/{username}/download", description="Download posts from insta and save in db")
async def accounts_download(username: str):
    return await download_posts(username)


@router.get("/accounts/{username}/posts")
async def list_accounts(username: str, session: AsyncSession = Depends(get_session)):
    # get the posts and return
    return 'success'
