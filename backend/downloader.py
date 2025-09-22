import instaloader


def load_session(nickname: str, session_id: str, ds_user_id: str, csrftoken: str, mid: str, ig_did: str):
    Loader = instaloader.Instaloader()

    Loader.load_session(nickname, {
        "sessionid": session_id,
        "ds_user_id": ds_user_id,
        "csrftoken": csrftoken,
        "mid": mid,
        "ig_did": ig_did
    })
    print("Session has been loaded")

    return Loader
