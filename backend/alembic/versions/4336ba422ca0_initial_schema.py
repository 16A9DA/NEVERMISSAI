"""initial schema

Revision ID: 4336ba422ca0
Revises:
Create Date: 2026-07-21

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "4336ba422ca0"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("clerk_user_id", sa.String, nullable=False, unique=True, index=True),
        sa.Column("name", sa.String, nullable=True),
        sa.Column("email", sa.String, nullable=True),
        sa.Column("phone", sa.String, nullable=True),
        sa.Column("preferred_language", sa.String, nullable=False, server_default="en"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "contacts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("phone_number", sa.String, nullable=False, index=True),
        sa.Column("name", sa.String, nullable=True),
        sa.Column("relation_type", sa.String, nullable=False),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "permission_rules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("action", sa.String, nullable=False),
        sa.Column("effect", sa.String, nullable=False),
        sa.Column("condition_json", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "memory_profile",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("key", sa.String, nullable=False),
        sa.Column("value_json", postgresql.JSONB, nullable=False, server_default="{}"),
    )

    op.create_table(
        "calls",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("caller_number", sa.String, nullable=False),
        sa.Column("contact_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("contacts.id"), nullable=True),
        sa.Column("status", sa.String, nullable=False, server_default="ringing"),
        sa.Column("caller_id_result_json", postgresql.JSONB, nullable=True),
        sa.Column("intent_json", postgresql.JSONB, nullable=True),
        sa.Column("urgency_score", sa.Numeric, nullable=True),
        sa.Column("urgency_bucket", sa.String, nullable=True),
        sa.Column("scam_score", sa.Numeric, nullable=True),
        sa.Column("scam_reasons_json", postgresql.JSONB, nullable=True),
        sa.Column("started_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("ended_at", sa.DateTime, nullable=True),
    )

    op.create_table(
        "calendar_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("start_at", sa.DateTime, nullable=False),
        sa.Column("end_at", sa.DateTime, nullable=False),
        sa.Column("location", sa.String, nullable=True),
        sa.Column("source", sa.String, nullable=False, server_default="ai_created"),
        sa.Column("related_call_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("calls.id"), nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "call_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("call_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("calls.id"), nullable=False),
        sa.Column("event_type", sa.String, nullable=False),
        sa.Column("payload_json", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("ts", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "call_transcripts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("call_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("calls.id"), nullable=False),
        sa.Column("speaker", sa.String, nullable=False),
        sa.Column("text", sa.Text, nullable=False),
        sa.Column("lang", sa.String, nullable=False, server_default="en"),
        sa.Column("ts", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "call_summaries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("call_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("calls.id"), nullable=False, unique=True),
        sa.Column("summary_text", sa.Text, nullable=False),
        sa.Column("action_items_json", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("people_json", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("locations_json", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("deadlines_json", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("numbers_json", postgresql.JSONB, nullable=False, server_default="{}"),
    )

    op.create_table(
        "flagged_numbers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("phone_number", sa.String, nullable=False, index=True),
        sa.Column("reason", sa.Text, nullable=False),
        sa.Column("flagged_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "notifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("call_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("calls.id"), nullable=True),
        sa.Column("type", sa.String, nullable=False),
        sa.Column("payload_json", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("delivered_at", sa.DateTime, nullable=True),
    )


def downgrade() -> None:
    op.drop_table("notifications")
    op.drop_table("flagged_numbers")
    op.drop_table("call_summaries")
    op.drop_table("call_transcripts")
    op.drop_table("call_events")
    op.drop_table("calendar_events")
    op.drop_table("calls")
    op.drop_table("memory_profile")
    op.drop_table("permission_rules")
    op.drop_table("contacts")
    op.drop_table("users")
