import glob
import mimetypes
import os
from pathlib import Path
from urllib.parse import urlparse
from app.models.posts import Account, Post
from app.api.schemas.posts import ProcessingStatus, ProcessingStatusData
from app.api.schemas.auth import InstAuthModel
from app.utils.sse_safe import safe_sse
from app.services.redis import RedisManager

import uuid
import json
import time
import random
import asyncio
import instaloader

from fastapi import HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from instaloader import Post as PostLoader


async def _create_post(session: AsyncSession, post: Post):
    try:
        session.add(post)
        await session.commit()
        await session.refresh(post)
    except Exception:
        await session.rollback()


def _load_session(
    nickname: str,
    sessionid: str,
    ds_user_id: str,
    csrftoken: str,
    mid: str,
    ig_did: str
):
    Loader = instaloader.Instaloader()

    Loader.load_session(nickname, {
        "sessionid": sessionid,
        "ds_user_id": ds_user_id,
        "csrftoken": csrftoken,
        "mid": mid,
        "ig_did": ig_did
    })

    print("Session has been loaded")

    return Loader


async def _download_worker(
    username: str,
    account_id: int,
    total_posts: int,
    profile: instaloader.Profile,
    session: AsyncSession,
    redis_session: RedisManager
):
    iterator = profile.get_posts()
    downloaded_posts_count = 0
    percent = 0

    await redis_session.save('jobs', ProcessingStatusData(
        username=username,
        status=ProcessingStatus.STARTING,
        total_posts=total_posts,
        percent=percent
    ))

    for post_data in iterator:
        job: ProcessingStatusData = await redis_session.load('jobs', username)
        if job.is_canceled:
            await redis_session.save('jobs', ProcessingStatusData(
                username=username,
                is_canceled=job.is_canceled,
                status=ProcessingStatus.CANCELED,
                total_posts=total_posts,
                percent=percent
            ))
            break

        await _create_post(session, Post(
            account_id=account_id,
            shortcode=post_data.shortcode,
            date_utc=post_data.date_utc,
            caption=post_data.caption,
            likes=post_data.likes,
            comments=post_data.comments,
            url=post_data.url,
            video_url=post_data.video_url,
            typename=post_data.typename
        ))

        if downloaded_posts_count >= total_posts:
            break

        downloaded_posts_count += 1
        current_percent = round(
            (downloaded_posts_count / total_posts) * 100)

        if current_percent != percent:
            percent = current_percent
            await redis_session.save('jobs', ProcessingStatusData(
                username=username,
                status=ProcessingStatus.PROCESSING,
                total_posts=total_posts,
                percent=percent
            ))

        time.sleep(round(random.uniform(0.2, 0.4), 2))

    await redis_session.save('jobs', ProcessingStatusData(
        username=username,
        status=ProcessingStatus.COMPLETED,
        total_posts=total_posts,
        percent=percent
    ))


async def download_posts(username: str, session: AsyncSession, redis_session: RedisManager):
    inst_auth: InstAuthModel = await redis_session.load('auth')

    if not inst_auth:
        raise HTTPException(
            status_code=400, detail="Could not get inst auth. Please complete the inst auth")

    job: ProcessingStatusData = await redis_session.load('jobs', username)
    print(job.status.value)
    if job.status == ProcessingStatus.PROCESSING or job.status == ProcessingStatus.STARTING:
        raise HTTPException(
            status_code=400, detail="Downloading process already has been started")

    Loader = _load_session(**inst_auth.model_dump())

    try:
        profile = instaloader.Profile.from_username(Loader.context, username)
        total_posts = profile.mediacount
        print(f"Profile '{profile.username}': {total_posts} posts.")
    except Exception as error:
        raise HTTPException(
            status_code=400, detail=f"Could not load profile: {error}")

    accountResult = await session.execute(select(Account).where(Account.username == username))
    account = accountResult.scalar_one_or_none()

    if not account:
        account = Account(
            username=username,
            total_posts=total_posts
        )
        session.add(account)
        await session.commit()
        await session.refresh(account)

    asyncio.create_task(_download_worker(
        username,
        account.id,
        total_posts,
        profile,
        session,
        redis_session
    ))

    return {"job_id": username}


async def get_download_status(username: str, redis_session: RedisManager):

    async def get_status():
        while True:
            current_job: ProcessingStatusData = await redis_session.load('jobs', username)
            await asyncio.sleep(15)

            payload = json.dumps({
                "status": current_job.status.value,
                "total_posts": current_job.total_posts,
                "percent": current_job.percent
            })
            yield f"data: {payload}\n\n"

            if current_job.status == ProcessingStatus.COMPLETED or not current_job.status:
                break

    return StreamingResponse(safe_sse(get_status()), media_type="text/event-stream")


def _pick_media_file(folder: str) -> Path:
    p = Path(folder)
    if not p.exists() or not p.is_dir():
        raise HTTPException(status_code=404, detail="Target folder not found")

    # Prefer mp4 (case-insensitive)
    mp4_files = sorted(p.glob("*.mp4")) + sorted(p.glob("*.MP4"))
    if mp4_files:
        return mp4_files[0]

    # Otherwise, look for images (common extensions)
    image_files = []
    for ext in ("*.jpg", "*.jpeg", "*.png", "*.gif", "*.webp"):
        image_files.extend(sorted(p.glob(ext)))
        image_files.extend(sorted(p.glob(ext.upper())))
    if image_files:
        return image_files[0]

    raise HTTPException(
        status_code=404, detail="No media found in downloaded post")


def _shortcode_from_url(url: str) -> str:
    path = urlparse(url).path  # e.g. "/p/SHORTCODE/"
    parts = [p for p in path.split("/") if p]
    # parts => ["p","SHORTCODE"] or ["reel","SHORTCODE"]
    if len(parts) >= 2:
        return parts[1]
    raise ValueError("Cannot find shortcode in URL")


async def download_post_by_link(link: str, session: AsyncSession, redis_session: RedisManager):
    # L = Instaloader(download_video_thumbnails=False, save_metadata=False)
    inst_auth: InstAuthModel = await redis_session.load('auth')

    if not inst_auth:
        raise HTTPException(
            status_code=400, detail="Could not get inst auth. Please complete the inst auth")

    Loader = _load_session(**inst_auth.model_dump())

    shortcode = _shortcode_from_url(link)

    post = PostLoader.from_shortcode(Loader.context, shortcode)
    target_folder = f"downloads/{post.owner_username}_{shortcode}"
    os.makedirs(target_folder, exist_ok=True)

    path_target_folder = Path(target_folder)

    Loader.download_post(post, target=path_target_folder)
    print("Downloaded to:", target_folder)

    # media_files = glob.glob(os.path.join(
    #     target_folder, "*.jpg")) + glob.glob(os.path.join(target_folder, "*.mp4"))
    # if not media_files:
    #     raise HTTPException(
    #         status_code=404, detail="No media found in downloaded post")

    # file_path = media_files[0]
    # filename = os.path.basename(file_path)

    file_path = _pick_media_file(target_folder)
    media_type, _ = mimetypes.guess_type(str(file_path))
    if media_type is None:
        media_type = "video/mp4" if file_path.suffix.lower() == ".mp4" else "image/jpeg"

    return FileResponse(path=str(file_path), filename=file_path.name, media_type=media_type)

    # return FileResponse(
    #     path=file_path,
    #     filename=filename,
    #     media_type="video/mp4" if file_path.endswith(".mp4") else "image/jpeg",
    # )
