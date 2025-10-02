from app.api.models import InstaAuthModel
from app.api.controllers import download_posts, get_download_status
from app.db.database import get_session
from app.db.models import Account, Post
from app.redis_db.database import get_redis

from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

import json

router = APIRouter()


@router.get("/ping")
def root():
    return {"message": "pong!"}


@router.post("/set_inst_auth", description="Set insta auth for download posts")
async def set_inst_auth(body: InstaAuthModel, rdb=Depends(get_redis)):
    await rdb.set("inst_auth", body.model_dump_json(), ex=3600)
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
async def list_accounts_posts(username: str,  start_date=None, end_date=None, text=None, page: int = Query(1, ge=1, le=10_000), session: AsyncSession = Depends(get_session)):
    limit = 50
    stmt = select(Post)
    if username:
        stmt = stmt.join(Post.account).where(
            Post.account.has(username=username))
    if start_date:
        stmt = stmt.where(Post.date_utc >= start_date)
    if end_date:
        stmt = stmt.where(Post.date_utc <= end_date)
    # if text:
    #     stmt = stmt.where(Post.caption.ilike(f"%{text}%"))

    stmt = stmt.order_by(Post.date_utc.desc()).limit(
        limit).offset((limit * page) - limit)

    result = await session.execute(stmt)

    return result.scalars().all()


@router.get("/accounts/posts/{post_id}", description="Get the post by post id")
async def get_post(post_id: int, session: AsyncSession = Depends(get_session)):
    post = (await session.execute(select(Post).where(Post.id == post_id))).scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "id": post.id,
        "caption": post.caption,
        "typename": post.typename,
        "account_id": post.account_id,
        "username": post.account.username,
        "date_utc": post.date_utc,
        "url": post.url,
        "video_url": post.video_url,
    }


@router.get('/accounts/posts/download_status/{job_id}')
async def get_posts_download_status(job_id: str, rdb=Depends(get_redis)):
    return await get_download_status(job_id, rdb)
