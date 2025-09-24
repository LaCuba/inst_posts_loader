from app.api import routers
from app.db.database import init_db

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FastAPI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)
app.include_router(routers.router, prefix="/api")


@app.on_event("startup")
async def on_startup():
    await init_db()
