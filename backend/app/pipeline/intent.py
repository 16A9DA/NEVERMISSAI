from app.llm.base import LLMClient

INTENT_TYPES = [
    "interview", "delivery", "appointment", "reschedule_appointment", "cancel_appointment",
    "emergency", "spam", "support", "sales", "fraud", "personal", "business",
]

_SCHEMA = {"intent": "string", "confidence": "number"}


async def detect_intent(llm: LLMClient, transcript_text: str) -> dict:
    response = await llm.complete(
        messages=[
            {
                "role": "user",
                "content": (
                    f"Conversation so far:\n{transcript_text}\n\n"
                    f"Classify the caller's intent. Valid types: {', '.join(INTENT_TYPES)}.\n"
                    f"Respond as JSON: {_SCHEMA}"
                ),
            }
        ],
        system="You classify the intent of a phone caller from the transcript so far. Be concise.",
        json_schema=_SCHEMA,
    )
    parsed = response.json or {}
    return {
        "intent": parsed.get("intent", "personal"),
        "confidence": parsed.get("confidence", 0.5),
    }
