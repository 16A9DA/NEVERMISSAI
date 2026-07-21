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


async def reschedule_calendar_event(
    db: AsyncSession,
    context: CallContext,
    event_id: uuid.UUID,
    start_at: datetime,
    end_at: datetime,
) -> tuple[PermissionDecision, dict | None]:
    decision = await check(db, context.user_id, "schedule_meetings")
    context.permission_decisions.append(vars(decision))
    if not decision.allowed:
        return decision, None

    calendar = LocalCalendarProvider(db)
    event = await calendar.reschedule(event_id, start_at, end_at)
    return decision, {
        "id": str(event.id),
        "title": event.title,
        "start_at": event.start_at.isoformat(),
        "end_at": event.end_at.isoformat(),
        "location": event.location,
    }


async def cancel_calendar_event(
    db: AsyncSession,
    context: CallContext,
    event_id: uuid.UUID,
) -> PermissionDecision:
    decision = await check(db, context.user_id, "schedule_meetings")
    context.permission_decisions.append(vars(decision))
    if not decision.allowed:
        return decision

    calendar = LocalCalendarProvider(db)
    await calendar.cancel_event(event_id)
    return decision


def _is_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False
