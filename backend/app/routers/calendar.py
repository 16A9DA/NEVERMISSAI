from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import google_calendar
from app.config import get_settings
from app.db.models import User
from app.deps import get_current_user, get_current_user_from_query, get_db

settings = get_settings()
router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.get("/connect")
async def connect(user: User = Depends(get_current_user_from_query)):
    return RedirectResponse(google_calendar.authorization_url(user.id))


@router.get("/callback")
async def callback(code: str, state: str, db: AsyncSession = Depends(get_db)):
    await google_calendar.handle_callback(db, code, state)
    return RedirectResponse(f"{settings.FRONTEND_URL}/dashboard")


@router.get("/status")
async def status(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    account = await google_calendar.get_account(db, user.id)
    if account is None:
        return {"connected": False, "email": None}
    return {"connected": True, "email": account.google_email}


@router.get("/events")
async def list_events(
    start: datetime | None = None,
    end: datetime | None = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    access_token = await google_calendar.get_valid_access_token(db, user.id)
    if access_token is None:
        raise HTTPException(400, "Google Calendar not connected")

    now = datetime.now(timezone.utc)
    time_min = start or now - timedelta(days=7)
    time_max = end or now + timedelta(days=30)
    events = await google_calendar.list_events(access_token, time_min, time_max)
    return [
        {
            "id": event["id"],
            "title": event.get("summary", ""),
            "description": event.get("description"),
            "start_at": event.get("start", {}).get("dateTime") or event.get("start", {}).get("date"),
            "end_at": event.get("end", {}).get("dateTime") or event.get("end", {}).get("date"),
        }
        for event in events
    ]


@router.post("/events")
async def create_event(
    title: str,
    start_at: datetime,
    end_at: datetime,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    access_token = await google_calendar.get_valid_access_token(db, user.id)
    if access_token is None:
        raise HTTPException(400, "Google Calendar not connected")
    return await google_calendar.create_event(access_token, title, start_at, end_at)


@router.delete("/events/{event_id}")
async def delete_event(
    event_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    access_token = await google_calendar.get_valid_access_token(db, user.id)
    if access_token is None:
        raise HTTPException(400, "Google Calendar not connected")
    await google_calendar.delete_event(access_token, event_id)
    return {"ok": True}
