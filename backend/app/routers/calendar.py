import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import google_calendar
from app.config import get_settings
from app.db.models import Booking, User
from app.deps import get_current_user, get_current_user_from_query, get_db

_LOCAL_PREFIX = "local-"

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
    now = datetime.now(timezone.utc)
    time_min = start or now - timedelta(days=7)
    time_max = end or now + timedelta(days=30)

    result = await db.execute(
        select(Booking).where(
            Booking.user_id == user.id,
            Booking.status != "cancelled",
            Booking.start_at >= time_min,
            Booking.start_at <= time_max,
        )
    )
    local_events = [
        {
            "id": f"{_LOCAL_PREFIX}{b.id}",
            "title": b.title,
            "description": b.caller_number,
            "start_at": b.start_at.isoformat(),
            "end_at": b.end_at.isoformat() if b.end_at else None,
        }
        for b in result.scalars().all()
    ]

    access_token = await google_calendar.get_valid_access_token(db, user.id)
    if access_token is None:
        return local_events

    events = await google_calendar.list_events(access_token, time_min, time_max)
    google_events = [
        {
            "id": event["id"],
            "title": event.get("summary", ""),
            "description": event.get("description"),
            "start_at": event.get("start", {}).get("dateTime") or event.get("start", {}).get("date"),
            "end_at": event.get("end", {}).get("dateTime") or event.get("end", {}).get("date"),
        }
        for event in events
    ]
    return local_events + google_events


@router.post("/events")
async def create_event(
    title: str,
    start_at: datetime,
    end_at: datetime,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    access_token = await google_calendar.get_valid_access_token(db, user.id)
    if access_token is not None:
        return await google_calendar.create_event(access_token, title, start_at, end_at)

    booking = Booking(user_id=user.id, title=title, start_at=start_at, end_at=end_at)
    db.add(booking)
    await db.commit()
    await db.refresh(booking)
    return {"id": f"{_LOCAL_PREFIX}{booking.id}", "title": title, "start_at": start_at, "end_at": end_at}


@router.delete("/events/{event_id}")
async def delete_event(
    event_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if event_id.startswith(_LOCAL_PREFIX):
        try:
            booking_id = uuid.UUID(event_id.removeprefix(_LOCAL_PREFIX))
        except ValueError:
            raise HTTPException(404, "Booking not found")
        booking = await db.get(Booking, booking_id)
        if booking is None or booking.user_id != user.id:
            raise HTTPException(404, "Booking not found")
        booking.status = "cancelled"
        await db.commit()
        return {"ok": True}

    access_token = await google_calendar.get_valid_access_token(db, user.id)
    if access_token is None:
        raise HTTPException(400, "Google Calendar not connected")
    await google_calendar.delete_event(access_token, event_id)
    return {"ok": True}
