from app.models.posts import Account
from app.downloader import load_session, start_download
from app.api.schemas.posts import ProcessingStatus, ProcessingStatusData
from app.utils.sse_safe import safe_sse

import uuid
import json
import asyncio
import instaloader

from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def download_posts(username: str, session: AsyncSession, redis_session):
    value: str = await redis_session.get("inst_auth")

    if not value:
        raise HTTPException(
            status_code=400, detail="Could not get inst auth. Please complete the inst auth")

    data = json.loads(value)
    Loader = load_session(**data)

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

    job_id = str(uuid.uuid4())

    asyncio.create_task(start_download(job_id,
                                       account.id, total_posts, profile, session, redis_session))

    return {"job_id": job_id}


async def get_download_status(job_id: str, redis_session):

    async def get_status():
        while True:
            value: str = await redis_session.get(job_id)
            current_status = ProcessingStatusData.model_validate_json(value)
            await asyncio.sleep(15)

            payload = json.dumps({
                "status": current_status.status.value,
                "total_posts": current_status.total_posts,
                "percent": current_status.percent
            })
            yield f"data: {payload}\n\n"

            if current_status.status == ProcessingStatus.COMPLETED or not current_status.status:
                break

    return StreamingResponse(safe_sse(get_status()), media_type="text/event-stream")
