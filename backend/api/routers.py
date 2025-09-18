from backend.api.controllers import download_posts
from fastapi import APIRouter
from backend.api.models import InstaAuthModel, DownloadModel

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


@router.post("/download", description="Download posts from insta and save in db")
def download(body: DownloadModel):
    # Download posts and return downloaded percent
    download_posts(body.nickname)
