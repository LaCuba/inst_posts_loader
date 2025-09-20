from backend.downloader import load_session
from backend.api.models import ProcessingStatus

import json
import instaloader
import time
import random

from fastapi import HTTPException
from fastapi.responses import StreamingResponse


async def download_posts(username: str):
    Loader = load_session()
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

        for post in iterator:
            # write on the db

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
