import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app import google_calendar
from app.db.models import Booking
from app.permissions.engine import PermissionDecision, check
from app.pipeline.context import CallContext

_LOCAL_PREFIX = "local-"


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
        booking = await _create_booking(db, context, title, start_at, end_at)
        return decision, _booking_payload(booking)

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

    if event_id.startswith(_LOCAL_PREFIX):
        booking = await _get_booking(db, event_id)
        if booking is None:
            return decision, None
        booking.start_at = start_at
        booking.end_at = end_at
        await db.commit()
        return decision, _booking_payload(booking)

    access_token = await google_calendar.get_valid_access_token(db, context.user_id)
    if access_token is None:
        booking = await _create_booking(db, context, "Rescheduled meeting", start_at, end_at)
        return decision, _booking_payload(booking)

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

    if event_id.startswith(_LOCAL_PREFIX):
        booking = await _get_booking(db, event_id)
        if booking is not None:
            booking.status = "cancelled"
            await db.commit()
        return decision

    access_token = await google_calendar.get_valid_access_token(db, context.user_id)
    if access_token is None:
        return decision

    await google_calendar.delete_event(access_token, event_id)
    return decision


async def _create_booking(
    db: AsyncSession, context: CallContext, title: str, start_at: datetime, end_at: datetime
) -> Booking:
    booking = Booking(
        user_id=context.user_id,
        call_id=context.call_id,
        caller_number=context.caller_number,
        title=title,
        start_at=start_at,
        end_at=end_at,
    )
    db.add(booking)
    await db.commit()
    await db.refresh(booking)
    return booking


async def _get_booking(db: AsyncSession, event_id: str) -> Booking | None:
    try:
        booking_id = uuid.UUID(event_id.removeprefix(_LOCAL_PREFIX))
    except ValueError:
        return None
    return await db.get(Booking, booking_id)


def _booking_payload(booking: Booking) -> dict:
    return {
        "id": f"{_LOCAL_PREFIX}{booking.id}",
        "title": booking.title,
        "start_at": booking.start_at.isoformat(),
        "end_at": booking.end_at.isoformat() if booking.end_at else None,
    }


def _event_payload(event: dict) -> dict:
    return {
        "id": event["id"],
        "title": event.get("summary", ""),
        "start_at": event.get("start", {}).get("dateTime"),
        "end_at": event.get("end", {}).get("dateTime"),
    }
