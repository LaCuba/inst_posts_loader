from app.api.routers import accounts, auth, posts
from app.core.postgres import init_db

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FastAPI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(accounts.router, prefix="/api/accounts", tags=["Accounts"])
app.include_router(posts.router, prefix="/api/posts", tags=["Posts"])


@app.on_event("startup")
async def on_startup():
    await init_db()
