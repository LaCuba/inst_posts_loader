from app.models.posts import Post
from app.core.redis import get_redis
from app.core.postgres import get_session
from app.services.redis import RedisManager
from app.api.schemas.posts import DownloadPostPayload, ProcessingStatus, ProcessingStatusData
from app.services.posts import download_post_by_link, download_posts, get_download_status

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.get("/{post_id}", description="Get the post by post id")
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


@router.get("/download/{username}", description="Download posts from inst and save in db")
async def account_posts_download(
    username: str,
    session: AsyncSession = Depends(get_session),
    rdb: RedisManager = Depends(get_redis)
):
    return await download_posts(username, session, rdb)


@router.post("/download/post", description="Download post from inst by link")
async def download_post_by_link_route(
    body: DownloadPostPayload,
    session: AsyncSession = Depends(get_session),
    rdb: RedisManager = Depends(get_redis)
):
    return await download_post_by_link(body.link, session, rdb)


@router.get("/download/{username}/cancel", description="Stop posts downloading process")
async def stop_account_posts_download(username: str, rdb: RedisManager = Depends(get_redis)):
    current_job: ProcessingStatusData = await rdb.load('jobs', username)

    if not current_job:
        raise HTTPException(
            status_code=400, detail=f"Process with {username} was not started")

    current_job.is_canceled = True
    current_job.status = ProcessingStatus.CANCELED
    await rdb.save('jobs', current_job)
    return {
        "status": "canceled",
    }


@router.get("/list/{username}", description="Get the posts by username account")
async def list_accounts_posts(
    username: str,
    start_date=None,
    end_date=None,
    text=None,
    page: int = Query(1, ge=1, le=10_000),
    session: AsyncSession = Depends(get_session)
):
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


@router.get('/download_status/{username}')
async def get_posts_download_status(username: str, rdb: RedisManager = Depends(get_redis)):
    return await get_download_status(username, rdb)
