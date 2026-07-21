import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Contact
from app.llm.base import LLMClient

RELATION_TYPES = [
    "recruiter", "employer", "family", "delivery", "friend",
    "unknown", "bank", "government", "hospital", "school","university",
    "other"
]

_CLASSIFY_SCHEMA = {"relation_type": "string", "confidence": "number", "reasoning": "string"}


async def identify_caller(
    db: AsyncSession, llm: LLMClient, user_id: uuid.UUID, phone_number: str, opening_line: str
) -> dict:
    result = await db.execute(
        select(Contact).where(Contact.user_id == user_id, Contact.phone_number == phone_number)
    )
    contact = result.scalar_one_or_none()
    if contact is not None:
        return {
            "relation_type": contact.relation_type,
            "name": contact.name,
            "confidence": 1.0,
            "source": "contact_db",
            "contact_id": str(contact.id),
        }

    response = await llm.complete(
        messages=[
            {
                "role": "user",
                "content": (
                    f"An unknown caller just said: \"{opening_line}\"\n"
                    f"Classify who this caller most likely is. Valid types: {', '.join(RELATION_TYPES)}.\n"
                    f"Respond as JSON: {_CLASSIFY_SCHEMA}"
                ),
            }
        ],
        system="You identify phone callers from context clues in what they say. Be concise.",
        json_schema=_CLASSIFY_SCHEMA,
    )
    parsed = response.json or {}
    return {
        "relation_type": parsed.get("relation_type", "unknown"),
        "name": None,
        "confidence": parsed.get("confidence", 0.5),
        "source": "llm",
        "contact_id": None,
        "reasoning": parsed.get("reasoning"),
    }
