"""Calendar provider interface. The demo runs entirely on
local_provider.py (Postgres-backed) to avoid OAuth setup risk during the
hackathon window; a real Google Calendar provider is a noted seam here,
not built.
"""

import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CalendarEventData:
    id: uuid.UUID
    title: str
    start_at: datetime
    end_at: datetime
    location: str | None = None


class CalendarProvider(ABC):
    @abstractmethod
    async def list_events(self, user_id: uuid.UUID, start: datetime, end: datetime) -> list[CalendarEventData]:
        ...

    @abstractmethod
    async def check_conflict(self, user_id: uuid.UUID, start: datetime, end: datetime) -> bool:
        ...

    @abstractmethod
    async def create_event(
        self,
        user_id: uuid.UUID,
        title: str,
        start_at: datetime,
        end_at: datetime,
        location: str | None = None,
        related_call_id: uuid.UUID | None = None,
    ) -> CalendarEventData:
        ...

    @abstractmethod
    async def reschedule(self, event_id: uuid.UUID, start_at: datetime, end_at: datetime) -> CalendarEventData:
        ...
