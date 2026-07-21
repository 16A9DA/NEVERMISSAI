import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.calendar.base import CalendarEventData, CalendarProvider
from app.db.models import CalendarEvent


def _to_data(row: CalendarEvent) -> CalendarEventData:
    return CalendarEventData(
        id=row.id, title=row.title, start_at=row.start_at, end_at=row.end_at, location=row.location
    )


class LocalCalendarProvider(CalendarProvider):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def list_events(self, user_id: uuid.UUID, start: datetime, end: datetime) -> list[CalendarEventData]:
        result = await self._db.execute(
            select(CalendarEvent).where(
                CalendarEvent.user_id == user_id,
                CalendarEvent.start_at < end,
                CalendarEvent.end_at > start,
            )
        )
        return [_to_data(row) for row in result.scalars().all()]

    async def check_conflict(self, user_id: uuid.UUID, start: datetime, end: datetime) -> bool:
        events = await self.list_events(user_id, start, end)
        return len(events) > 0

    async def create_event(
        self,
        user_id: uuid.UUID,
        title: str,
        start_at: datetime,
        end_at: datetime,
        location: str | None = None,
        related_call_id: uuid.UUID | None = None,
    ) -> CalendarEventData:
        row = CalendarEvent(
            user_id=user_id,
            title=title,
            start_at=start_at,
            end_at=end_at,
            location=location,
            source="ai_created",
            related_call_id=related_call_id,
        )
        self._db.add(row)
        await self._db.commit()
        await self._db.refresh(row)
        return _to_data(row)

    async def reschedule(self, event_id: uuid.UUID, start_at: datetime, end_at: datetime) -> CalendarEventData:
        result = await self._db.execute(select(CalendarEvent).where(CalendarEvent.id == event_id))
        row = result.scalar_one()
        row.start_at = start_at
        row.end_at = end_at
        await self._db.commit()
        await self._db.refresh(row)
        return _to_data(row)

    async def cancel_event(self, event_id: uuid.UUID) -> None:
        result = await self._db.execute(select(CalendarEvent).where(CalendarEvent.id == event_id))
        row = result.scalar_one()
        await self._db.delete(row)
        await self._db.commit()
