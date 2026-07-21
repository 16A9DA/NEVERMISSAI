"""Seeds one demo user plus the contacts, permission rules, and memory
profile needed to run the four demo scenarios (recruiter, delivery,
hospital, scam) end to end via POST /demo/place-call.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.db.models import Contact, MemoryProfile, PermissionRule, User  # noqa: E402
from app.db.session import async_session_maker  # noqa: E402

DEMO_CLERK_USER_ID = "demo_user"

CONTACTS = [
    {"phone_number": "+15550100001", "name": "Jamie Reyes (TalentBridge)", "relation_type": "recruiter"},
    {"phone_number": "+15550100002", "name": "FastCourier Driver", "relation_type": "delivery"},
    {"phone_number": "+15550100003", "name": "St. Mary Hospital", "relation_type": "hospital"},
    {"phone_number": "+15550100004", "name": None, "relation_type": "unknown"},
]

PERMISSION_RULES = [
    ("schedule_meetings", "allow"),
    ("confirm_interview_times", "allow"),
    ("reschedule_appointments", "allow"),
    ("accept_deliveries", "allow"),
    ("translate_conversations", "allow"),
    ("take_messages", "allow"),
    ("reveal_passwords", "deny"),
    ("reveal_personal_id", "deny"),
    ("accept_payments", "deny"),
    ("agree_to_contracts", "deny"),
]

MEMORY_PROFILE = [
    ("preferred_working_hours", {"start": "09:00", "end": "18:00", "timezone": "UTC"}),
    ("languages", {"spoken": ["en", "ar"]}),
]


async def seed() -> None:
    async with async_session_maker() as session:
        user = User(clerk_user_id=DEMO_CLERK_USER_ID, name="Demo User", preferred_language="en")
        session.add(user)
        await session.flush()

        for c in CONTACTS:
            session.add(Contact(user_id=user.id, **c))

        for action, effect in PERMISSION_RULES:
            session.add(PermissionRule(user_id=user.id, action=action, effect=effect))

        for key, value in MEMORY_PROFILE:
            session.add(MemoryProfile(user_id=user.id, key=key, value_json=value))

        await session.commit()
        print(f"Seeded demo user {user.id} ({DEMO_CLERK_USER_ID}) with 4 contacts, "
              f"{len(PERMISSION_RULES)} permission rules, {len(MEMORY_PROFILE)} memory entries.")


if __name__ == "__main__":
    asyncio.run(seed())
