from app.llm.base import LLMClient

ACTION_TYPES = ["book", "reschedule", "cancel", "callback_request", "leave_information", "none"]

_SCHEMA = {"action": "string", "confidence": "number"}


async def detect_action(llm: LLMClient, transcript_text: str) -> dict:
    response = await llm.complete(
        messages=[
            {
                "role": "user",
                "content": (
                    f"Conversation so far:\n{transcript_text}\n\n"
                    f"Classify what the caller wants done. Valid types: {', '.join(ACTION_TYPES)}.\n"
                    f"Respond as JSON: {_SCHEMA}"
                ),
            }
        ],
        system="You classify what action a phone caller wants taken, separate from why they're calling. Be concise.",
        json_schema=_SCHEMA,
    )
    parsed = response.json or {}
    return {
        "action": parsed.get("action", "none"),
        "confidence": parsed.get("confidence", 0.5),
    }
