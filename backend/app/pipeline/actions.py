from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app import google_calendar
from app.permissions.engine import PermissionDecision, check
from app.pipeline.context import CallContext

_NOT_CONNECTED = PermissionDecision(
    action="schedule_meetings", allowed=False, reason="Google Calendar not connected"
)


async def create_calendar_event(
    db: AsyncSession,
    context: CallContext,
    title: str,
    start_at: datetime,
    end_at: datetime,
) -> tuple[PermissionDecision, dict | None]:
    decision = await check(db, context.user_id, "schedule_meetings")
    context.permission_decisions.append(vars(decision))
    if not decision.allowed:
        return decision, None

    access_token = await google_calendar.get_valid_access_token(db, context.user_id)
    if access_token is None:
        return _NOT_CONNECTED, None

    event = await google_calendar.create_event(access_token, title, start_at, end_at)
    return decision, _event_payload(event)


async def reschedule_calendar_event(
    db: AsyncSession,
    context: CallContext,
    event_id: str,
    start_at: datetime,
    end_at: datetime,
) -> tuple[PermissionDecision, dict | None]:
    decision = await check(db, context.user_id, "schedule_meetings")
    context.permission_decisions.append(vars(decision))
    if not decision.allowed:
        return decision, None

    access_token = await google_calendar.get_valid_access_token(db, context.user_id)
    if access_token is None:
        return _NOT_CONNECTED, None

    event = await google_calendar.patch_event(access_token, event_id, start_at, end_at)
    return decision, _event_payload(event)


async def cancel_calendar_event(
    db: AsyncSession,
    context: CallContext,
    event_id: str,
) -> PermissionDecision:
    decision = await check(db, context.user_id, "schedule_meetings")
    context.permission_decisions.append(vars(decision))
    if not decision.allowed:
        return decision

    access_token = await google_calendar.get_valid_access_token(db, context.user_id)
    if access_token is None:
        return _NOT_CONNECTED

    await google_calendar.delete_event(access_token, event_id)
    return decision


def _event_payload(event: dict) -> dict:
    return {
        "id": event["id"],
        "title": event.get("summary", ""),
        "start_at": event.get("start", {}).get("dateTime"),
        "end_at": event.get("end", {}).get("dateTime"),
    }
