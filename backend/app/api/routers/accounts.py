from app.core.postgres import get_session
from app.models.posts import Account

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.get("/", description="Get the exists accounts")
async def list_accounts(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Account))
    return result.scalars().all()
