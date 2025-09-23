from backend.api.models import InstaAuthModel
from backend.api.controllers import download_posts
from backend.db.database import get_session
from backend.db.models import Account, Post
from backend.redis_db.database import get_redis

from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import json

router = APIRouter()


@router.get("/ping")
def root():
    return {"message": "pong!"}


@router.post("/set_inst_auth", description="Set insta auth for download posts")
async def set_inst_auth(body: InstaAuthModel, rdb=Depends(get_redis)):
    await rdb.set("inst_auth", json.dumps(body), ex=3600)
    return {
        "status": "ok",
    }


@router.get("/accounts", description="Get the exists accounts")
async def list_accounts(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Account))
    return result.scalars().all()


@router.get("/accounts/{username}/download", description="Download posts from insta and save in db")
async def accounts_download(username: str, session: AsyncSession = Depends(get_session), rdb=Depends(get_redis)):
    return await download_posts(username, session, rdb)


@router.get("/accounts/{username}/posts", description="Get the posts by username account")
async def list_accounts_posts(username: str,  start_date=None, end_date=None, text=None, page=1, session: AsyncSession = Depends(get_session)):
    limit = 50

    stmt = select(Post)
    if username:
        stmt = stmt.join(Post.account).where(
            Post.account.has(username=username))
    if start_date:
        stmt = stmt.where(Post.date_utc >= start_date)
    if end_date:
        stmt = stmt.where(Post.date_utc <= end_date)
    if text:
        stmt = stmt.where(Post.caption.ilike(f"%{text}%"))

    stmt = stmt.order_by(Post.date_utc.desc()).limit(
        limit).offset(limit * page)

    return session.execute(stmt).scalars().all()


@router.get("/accounts/posts/{post_id}", description="Get the post by post id")
async def get_post(post_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "id": post.id,
        "caption": post.caption,
        "typename": post.typename,
        "account_id": post.account_id,
        "created_at": post.created_at,
        "url": post.url,
        "video_url": post.video_url,
    }
