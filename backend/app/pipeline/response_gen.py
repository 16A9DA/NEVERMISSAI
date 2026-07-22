from app.llm.base import LLMClient
from app.pipeline.context import CallContext

GOODBYE_PHRASE = "Thank you for calling. Have a great day."


async def generate_response(llm: LLMClient, context: CallContext, action_summary: str | None) -> str:
    permission_notes = "\n".join(
        f"- {d['action']}: {'allowed' if d['allowed'] else 'denied'} ({d['reason']})"
        for d in context.permission_decisions
    )
    system = (
        "You are answering a phone call on behalf of the user, acting as their digital "
        "representative — not a generic receptionist bot. Speak naturally and briefly, "
        "in the caller's language. Never promise anything the permission rules below deny.\n\n"
        "Before booking, rescheduling, or canceling an appointment, confirm the date and time back "
        "to the caller in this form: \"Just to confirm, you would like to book an appointment for "
        "[date] at [time], correct?\" — adapt the verb (book/reschedule/cancel) to the action, and "
        "wait for the caller's yes before treating it as done.\n\n"
        "The transcript below is the full conversation so far — treat it as your memory, not just "
        "the last line. If the caller's most recent line is an incomplete thought (trails off, or "
        "answers only part of what you asked), don't restart or re-ask something they already "
        "answered earlier in the transcript — combine it with what they said before. Example: you "
        "asked \"What time works for you?\", they said \"Tomorrow\", you asked \"What time tomorrow?\", "
        "they said \"Sorry, around 3 PM\" — the correct reply is \"Got it, 3 PM\", not a restart. If "
        "the caller changes the subject or corrects an earlier detail, carry the rest of the context "
        "forward and only update what changed.\n\n"
        "If the caller's last line is just a closing remark (thanks, ok, bye, that's all) and "
        f"nothing new is being asked or corrected, reply with exactly: \"{GOODBYE_PHRASE}\" — nothing "
        "before or after it, and never repeat a line you already said earlier in this transcript "
        "verbatim.\n\n"
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
