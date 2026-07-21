import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.calendar.local_provider import LocalCalendarProvider
from app.permissions.engine import PermissionDecision, check
from app.pipeline.context import CallContext


async def create_calendar_event(
    db: AsyncSession,
    context: CallContext,
    title: str,
    start_at: datetime,
    end_at: datetime,
    location: str | None = None,
) -> tuple[PermissionDecision, dict | None]:
    """Schedules a calendar event, gated by the permission engine. Returns
    the permission decision plus the created event data (None if denied)."""
    decision = await check(db, context.user_id, "schedule_meetings")
    context.permission_decisions.append(vars(decision))
    if not decision.allowed:
        return decision, None

    calendar = LocalCalendarProvider(db)
    event = await calendar.create_event(
        user_id=context.user_id,
        title=title,
        start_at=start_at,
        end_at=end_at,
        location=location,
        related_call_id=uuid.UUID(context.call_id) if _is_uuid(context.call_id) else None,
    )
    return decision, {
        "id": str(event.id),
        "title": event.title,
        "start_at": event.start_at.isoformat(),
        "end_at": event.end_at.isoformat(),
        "location": event.location,
    }


def _is_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False
