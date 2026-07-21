import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import CallSummary
from app.llm.base import LLMClient
from app.pipeline.context import CallContext

_SCHEMA = {
    "summary": "string",
    "action_items": ["string"],
    "people": ["string"],
    "locations": ["string"],
    "deadlines": ["string"],
    "numbers": ["string"],
}


async def generate_summary(db: AsyncSession, llm: LLMClient, context: CallContext) -> CallSummary:
    response = await llm.complete(
        messages=[
            {
                "role": "user",
                "content": (
                    f"Call transcript:\n{context.transcript_text()}\n\n"
                    f"Summarize this call. Respond as JSON: {_SCHEMA}"
                ),
            }
        ],
        system="You write concise call summaries for someone who missed the call.",
        json_schema=_SCHEMA,
    )
    parsed = response.json or {}

    row = CallSummary(
        call_id=uuid.UUID(context.call_id),
        summary_text=parsed.get("summary", response.text.strip()),
        action_items_json={"items": parsed.get("action_items", [])},
        people_json={"items": parsed.get("people", [])},
        locations_json={"items": parsed.get("locations", [])},
        deadlines_json={"items": parsed.get("deadlines", [])},
        numbers_json={"items": parsed.get("numbers", [])},
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row
