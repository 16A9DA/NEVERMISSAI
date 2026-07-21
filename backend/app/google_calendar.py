import uuid
from datetime import datetime, timedelta, timezone

import httpx
from cryptography.fernet import Fernet
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db.models import GoogleCalendarAccount

settings = get_settings()

_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
_TOKEN_URL = "https://oauth2.googleapis.com/token"
_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
_EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
_SCOPE = "https://www.googleapis.com/auth/calendar"


def _fernet() -> Fernet:
    return Fernet(settings.TOKEN_ENCRYPTION_KEY.encode())


def encrypt_state(user_id: uuid.UUID) -> str:
    return _fernet().encrypt(str(user_id).encode()).decode()


def decrypt_state(state: str) -> uuid.UUID:
    return uuid.UUID(_fernet().decrypt(state.encode()).decode())


def authorization_url(user_id: uuid.UUID) -> str:
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": _SCOPE,
        "access_type": "offline",
        "prompt": "consent",
        "state": encrypt_state(user_id),
    }
    return f"{_AUTH_URL}?{httpx.QueryParams(params)}"


async def handle_callback(db: AsyncSession, code: str, state: str) -> GoogleCalendarAccount:
    user_id = decrypt_state(state)
    async with httpx.AsyncClient() as client:
        token_res = await client.post(
            _TOKEN_URL,
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        token_res.raise_for_status()
        tokens = token_res.json()

        userinfo_res = await client.get(
            _USERINFO_URL, headers={"Authorization": f"Bearer {tokens['access_token']}"}
        )
        userinfo_res.raise_for_status()
        email = userinfo_res.json().get("email", "")

    fernet = _fernet()
    expiry = datetime.now(timezone.utc) + timedelta(seconds=tokens.get("expires_in", 3600))

    result = await db.execute(select(GoogleCalendarAccount).where(GoogleCalendarAccount.user_id == user_id))
    account = result.scalar_one_or_none()
    if account is None:
        account = GoogleCalendarAccount(user_id=user_id)
        db.add(account)

    account.google_email = email
    account.access_token_encrypted = fernet.encrypt(tokens["access_token"].encode()).decode()
    if tokens.get("refresh_token"):
        account.refresh_token_encrypted = fernet.encrypt(tokens["refresh_token"].encode()).decode()
    account.token_expiry = expiry
    await db.commit()
    await db.refresh(account)
    return account


async def get_account(db: AsyncSession, user_id: uuid.UUID) -> GoogleCalendarAccount | None:
    result = await db.execute(select(GoogleCalendarAccount).where(GoogleCalendarAccount.user_id == user_id))
    return result.scalar_one_or_none()


async def get_valid_access_token(db: AsyncSession, user_id: uuid.UUID) -> str | None:
    account = await get_account(db, user_id)
    if account is None:
        return None
    fernet = _fernet()
    if account.token_expiry > datetime.now(timezone.utc) + timedelta(seconds=30):
        return fernet.decrypt(account.access_token_encrypted.encode()).decode()

    refresh_token = fernet.decrypt(account.refresh_token_encrypted.encode()).decode()
    async with httpx.AsyncClient() as client:
        res = await client.post(
            _TOKEN_URL,
            data={
                "refresh_token": refresh_token,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "grant_type": "refresh_token",
            },
        )
        res.raise_for_status()
        tokens = res.json()

    account.access_token_encrypted = fernet.encrypt(tokens["access_token"].encode()).decode()
    account.token_expiry = datetime.now(timezone.utc) + timedelta(seconds=tokens.get("expires_in", 3600))
    await db.commit()
    return tokens["access_token"]


async def list_events(access_token: str, time_min: datetime, time_max: datetime) -> list[dict]:
    async with httpx.AsyncClient() as client:
        res = await client.get(
            _EVENTS_URL,
            headers={"Authorization": f"Bearer {access_token}"},
            params={
                "timeMin": time_min.isoformat(),
                "timeMax": time_max.isoformat(),
                "singleEvents": "true",
                "orderBy": "startTime",
            },
        )
        res.raise_for_status()
        return res.json().get("items", [])


async def create_event(access_token: str, summary: str, start_at: datetime, end_at: datetime) -> dict:
    async with httpx.AsyncClient() as client:
        res = await client.post(
            _EVENTS_URL,
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "summary": summary,
                "start": {"dateTime": start_at.isoformat()},
                "end": {"dateTime": end_at.isoformat()},
            },
        )
        res.raise_for_status()
        return res.json()


async def patch_event(access_token: str, event_id: str, start_at: datetime, end_at: datetime) -> dict:
    async with httpx.AsyncClient() as client:
        res = await client.patch(
            f"{_EVENTS_URL}/{event_id}",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "start": {"dateTime": start_at.isoformat()},
                "end": {"dateTime": end_at.isoformat()},
            },
        )
        res.raise_for_status()
        return res.json()


async def delete_event(access_token: str, event_id: str) -> None:
    async with httpx.AsyncClient() as client:
        res = await client.delete(
            f"{_EVENTS_URL}/{event_id}", headers={"Authorization": f"Bearer {access_token}"}
        )
        if res.status_code not in (204, 410, 404):
            res.raise_for_status()
