import json
import random
import time
import instaloader

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Post
from app.api.models import ProcessingStatus


async def create_post(session: AsyncSession, post: Post):
    try:
        session.add(post)
        await session.commit()
        await session.refresh(post)
    except Exception:
        await session.rollback()


def load_session(nickname: str, sessionid: str, ds_user_id: str, csrftoken: str, mid: str, ig_did: str):
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


async def start_download(job_id: str, account_id: int, total_posts: int, profile: instaloader.Profile, session: AsyncSession, redis_session):
    iterator = profile.get_posts()
    downloaded_posts_count = 0
    percent = 0

    await redis_session.set(job_id, json.dumps({
        "status": ProcessingStatus.STARTING,
        "total_posts": total_posts,
        "percent": percent
    }))

    for post_data in iterator:
        print('--------------------------------> post_data')
        post = Post(account_id=account_id, shortcode=post_data.shortcode, date_utc=post_data.date_utc, caption=post_data.caption,
                    likes=post_data.likes, comments=post_data.comments, url=post_data.url, video_url=post_data.video_url, typename=post_data.typename)

        await create_post(session, post)

        if downloaded_posts_count >= total_posts:
            break

        downloaded_posts_count += 1
        current_percent = round(
            (downloaded_posts_count / total_posts) * 100, 2)

        if current_percent != percent and current_percent % 2:
            await redis_session.set(job_id, json.dumps({
                "status": ProcessingStatus.PROCESSING,
                "total_posts": total_posts,
                "percent": percent
            }))

        time.sleep(round(random.uniform(0.2, 0.4), 2))

    await redis_session.set(job_id, json.dumps({
        "status": ProcessingStatus.COMPLETED,
        "total_posts": total_posts,
        "percent": percent
    }))
