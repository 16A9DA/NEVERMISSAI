from typing import AsyncGenerator

import chromadb
from fastapi import Depends, Header, HTTPException, status
from jose import jwt
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db.models import User
from app.db.session import async_session_maker

settings = get_settings()

DEV_FALLBACK_CLERK_USER_ID = "demo_user"

_redis: Redis | None = None
_chroma_client: chromadb.ClientAPI | None = None


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


def get_redis() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis


def get_chroma() -> chromadb.ClientAPI:
    global _chroma_client
    if _chroma_client is None:
        host, _, port = settings.CHROMA_URL.replace("http://", "").partition(":")
        _chroma_client = chromadb.HttpClient(host=host, port=int(port or 8000))
    return _chroma_client


def decode_clerk_token(token: str) -> str:
    try:
        claims = jwt.get_unverified_claims(token)
    except Exception as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token") from exc
    sub = claims.get("sub")
    if not sub:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token missing sub claim")
    return sub


async def get_current_user_id(authorization: str = Header(default="")) -> str:
    if not authorization.startswith("Bearer "):
        if settings.ENV == "dev":
            return DEV_FALLBACK_CLERK_USER_ID
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing bearer token")
    return decode_clerk_token(authorization.removeprefix("Bearer "))


async def get_current_user_id_ws(token: str | None = None) -> str:
    if not token:
        if settings.ENV == "dev":
            return DEV_FALLBACK_CLERK_USER_ID
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing token query param")
    return decode_clerk_token(token)


async def _get_or_create_user(clerk_user_id: str, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.clerk_user_id == clerk_user_id))
    user = result.scalar_one_or_none()
    if user is None:
        user = User(clerk_user_id=clerk_user_id)
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return user


async def get_current_user(
    clerk_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> User:
    return await _get_or_create_user(clerk_user_id, db)


async def get_current_user_from_query(
    clerk_user_id: str = Depends(get_current_user_id_ws),
    db: AsyncSession = Depends(get_db),
) -> User:
    return await _get_or_create_user(clerk_user_id, db)


async def get_call_owner(db: AsyncSession = Depends(get_db)) -> User:
    """Incoming Twilio calls carry no Clerk auth, so they can't resolve to
    'whoever is logged in'. Attribute them to the one real registered
    account instead of the anonymous dev fallback user."""
    result = await db.execute(select(User).where(User.clerk_user_id != DEV_FALLBACK_CLERK_USER_ID).order_by(User.id))
    user = result.scalars().first()
    if user is not None:
        return user
    return await _get_or_create_user(DEV_FALLBACK_CLERK_USER_ID, db)
