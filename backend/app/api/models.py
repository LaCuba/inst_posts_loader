from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class InstaAuthModel(BaseModel):
    nickname: str
    sessionid: str
    ds_user_id: str
    csrftoken: str
    mid: str
    ig_did: str


# class DownloadModel(BaseModel):
#     nickname: str
#     count_of_posts: int
#     count_of_skip: int = 0
#     max_posts: Optional[int] = Field(None)
#     chunk_size: int = Field(100)


class ProcessingStatus(str, Enum):
    STARTING = 'starting'
    PROCESSING = 'processing'
    COMPLETED = 'completed'


class ProcessingStatusData(BaseModel):
    status: ProcessingStatus
    total_posts: int
    percent: int
