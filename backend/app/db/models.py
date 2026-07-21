import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.session import Base


def uuid_pk() -> Mapped[uuid.UUID]:
    return mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = uuid_pk()
    clerk_user_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=True)
    phone: Mapped[str] = mapped_column(String, nullable=True)
    preferred_language: Mapped[str] = mapped_column(String, default="en")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    contacts: Mapped[list["Contact"]] = relationship(back_populates="user")


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[uuid.UUID] = uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    phone_number: Mapped[str] = mapped_column(String, index=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    relation_type: Mapped[str] = mapped_column(String)  # recruiter|employer|family|delivery|friend|bank|government|hospital|school|unknown
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="contacts")


class PermissionRule(Base):
    __tablename__ = "permission_rules"

    id: Mapped[uuid.UUID] = uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String)
    effect: Mapped[str] = mapped_column(String)  # allow|deny
    condition_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class MemoryProfile(Base):
    __tablename__ = "memory_profile"

    id: Mapped[uuid.UUID] = uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    key: Mapped[str] = mapped_column(String)
    value_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    id: Mapped[uuid.UUID] = uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String)
    start_at: Mapped[datetime] = mapped_column()
    end_at: Mapped[datetime] = mapped_column()
    location: Mapped[str] = mapped_column(String, nullable=True)
    source: Mapped[str] = mapped_column(String, default="ai_created")  # ai_created|manual
    related_call_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("calls.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Call(Base):
    __tablename__ = "calls"

    id: Mapped[uuid.UUID] = uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    caller_number: Mapped[str] = mapped_column(String)
    contact_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("contacts.id"), nullable=True)
    status: Mapped[str] = mapped_column(String, default="ringing")  # ringing|active|completed
    caller_id_result_json: Mapped[dict] = mapped_column(JSONB, nullable=True)
    intent_json: Mapped[dict] = mapped_column(JSONB, nullable=True)
    urgency_score: Mapped[int] = mapped_column(Numeric, nullable=True)
    urgency_bucket: Mapped[str] = mapped_column(String, nullable=True)  # green|yellow|orange|red
    scam_score: Mapped[int] = mapped_column(Numeric, nullable=True)
    scam_reasons_json: Mapped[dict] = mapped_column(JSONB, nullable=True)
    started_at: Mapped[datetime] = mapped_column(server_default=func.now())
    ended_at: Mapped[datetime] = mapped_column(nullable=True)


class CallEvent(Base):
    __tablename__ = "call_events"

    id: Mapped[uuid.UUID] = uuid_pk()
    call_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("calls.id"))
    event_type: Mapped[str] = mapped_column(String)
    payload_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    ts: Mapped[datetime] = mapped_column(server_default=func.now())


class CallTranscript(Base):
    __tablename__ = "call_transcripts"

    id: Mapped[uuid.UUID] = uuid_pk()
    call_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("calls.id"))
    speaker: Mapped[str] = mapped_column(String)  # caller|ai
    text: Mapped[str] = mapped_column(Text)
    lang: Mapped[str] = mapped_column(String, default="en")
    ts: Mapped[datetime] = mapped_column(server_default=func.now())


class CallSummary(Base):
    __tablename__ = "call_summaries"

    id: Mapped[uuid.UUID] = uuid_pk()
    call_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("calls.id"), unique=True)
    summary_text: Mapped[str] = mapped_column(Text)
    action_items_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    people_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    locations_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    deadlines_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    numbers_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class FlaggedNumber(Base):
    __tablename__ = "flagged_numbers"

    id: Mapped[uuid.UUID] = uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    phone_number: Mapped[str] = mapped_column(String, index=True)
    reason: Mapped[str] = mapped_column(Text)
    flagged_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[uuid.UUID] = uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    call_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("calls.id"), nullable=True)
    type: Mapped[str] = mapped_column(String)  # emergency|summary|scam_alert
    payload_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    delivered_at: Mapped[datetime] = mapped_column(nullable=True)
