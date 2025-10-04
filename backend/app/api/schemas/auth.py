from pydantic import BaseModel


class InstAuthModel(BaseModel):
    nickname: str
    sessionid: str
    ds_user_id: str
    csrftoken: str
    mid: str
    ig_did: str
