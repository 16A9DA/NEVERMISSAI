from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.calendar.local_provider import LocalCalendarProvider
from app.db.models import User
from app.deps import get_current_user, get_db

router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.get("/events")
async def list_events(
    start: datetime | None = None,
    end: datetime | None = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    now = datetime.now(timezone.utc)
    range_start = start or now - timedelta(days=7)
    range_end = end or now + timedelta(days=30)

    calendar = LocalCalendarProvider(db)
    events = await calendar.list_events(user.id, range_start, range_end)
    return [
        {
            "id": str(event.id),
            "title": event.title,
            "start_at": event.start_at.isoformat(),
            "end_at": event.end_at.isoformat(),
            "location": event.location,
        }
        for event in events
    ]
