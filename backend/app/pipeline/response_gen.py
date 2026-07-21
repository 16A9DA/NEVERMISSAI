from app.llm.base import LLMClient
from app.pipeline.context import CallContext

# TODO(memory): once ChromaDB long-term memory is wired up (Phase 5 per the
# build plan), retrieved past-conversation snippets get injected into the
# system prompt here. For now context.memory_hits is always empty.


async def generate_response(llm: LLMClient, context: CallContext, action_summary: str | None) -> str:
    """Generates the AI's next spoken line, acting as the user's digital
    representative — aware of what it just identified/decided/did, and
    bound by whatever the permission engine allowed."""
    permission_notes = "\n".join(
        f"- {d['action']}: {'allowed' if d['allowed'] else 'denied'} ({d['reason']})"
        for d in context.permission_decisions
    )
    system = (
        "You are answering a phone call on behalf of the user, acting as their digital "
        "representative — not a generic receptionist bot. Speak naturally and briefly, "
        "in the caller's language. Never promise anything the permission rules below deny.\n\n"
        f"Caller identified as: {context.caller_id_result}\n"
        f"Detected intent: {context.intent}\n"
        f"Permission decisions this call:\n{permission_notes or '(none yet)'}\n"
        f"Action just taken: {action_summary or '(none yet)'}"
    )
    response = await llm.complete(
        messages=[{"role": "user", "content": context.transcript_text()}],
        system=system,
    )
    return response.text.strip()
