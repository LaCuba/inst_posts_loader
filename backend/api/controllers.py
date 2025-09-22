from backend.db.models import Account, Post
from backend.downloader import load_session
from backend.api.models import ProcessingStatus

import json
import instaloader
import time
import random

from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession


async def download_posts(username: str, session: AsyncSession, redis_session):
    value = await redis_session.get("inst_auth")
    Loader = load_session(**value)
    try:
        profile = instaloader.Profile.from_username(Loader.context, username)
        total_posts = profile.mediacount
        print(f"Profile '{profile.username}': {total_posts} posts.")
    except Exception as error:
        raise HTTPException(
            status_code=400, detail=f"Could not load profile: {error}")

    async def event_generator():
        iterator = profile.get_posts()
        downloaded_posts_count = 0
        percent = 0

        yield json.dumps({
            "status": ProcessingStatus.STARTING,
            "total_posts": total_posts,
            "percent": percent
        })
        account = Account(
            username=username,
            total_posts=total_posts
        )
        session.add(account)
        await session.commit()

        for post in iterator:
            session.add(Post(account_id=account.id, **post))
            await session.commit()

            if downloaded_posts_count >= total_posts:
                break

            downloaded_posts_count += 1
            current_percent = round(
                (downloaded_posts_count / total_posts) * 100, 2)

            if current_percent != percent and current_percent % 2:
                yield json.dumps({
                    "status": ProcessingStatus.PROCESSING,
                    "total_posts": total_posts,
                    "percent": percent
                })

            time.sleep(round(random.uniform(0.2, 0.4), 2))

        yield json.dumps({"status": ProcessingStatus.COMPLETED, "total_posts": total_posts, "percent": percent}) + "\n"

    return StreamingResponse(event_generator(), media_type="application/json")
