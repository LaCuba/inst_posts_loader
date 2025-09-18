

from backend.downloader import load_session

import instaloader
import asyncio

from fastapi import HTTPException


async def download_posts(username: str):
    Loader = load_session()
    try:
        profile = instaloader.Profile.from_username(Loader.context, username)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Could not load profile: {e}")

    # loop = asyncio.get_event_loop()
    # TODO: Create loader with chunks
