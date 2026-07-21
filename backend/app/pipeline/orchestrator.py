import asyncio
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Call, CallEvent, CallTranscript
from app.llm.factory import get_llm_client
from app.pipeline import caller_id, intent as intent_stage, response_gen, summary
from app.pipeline.actions import cancel_calendar_event, create_calendar_event, reschedule_calendar_event
from app.pipeline.context import CallContext, TranscriptTurn
from app.voice.factory import get_stt, get_tts
from app.voice.transport.base import CallTransport
from app.ws.events import EventType
from app.ws.manager import manager

_MEETING_SLOT_SCHEMA = {"start_at_iso": "string", "duration_minutes": "number"}
_GREETING = "Hi, this is Ryan's AI assistant. How can I help you?"


class CallPipeline:
    def __init__(self, db: AsyncSession, user_id: uuid.UUID, transport: CallTransport):
        self._db = db
        self._user_id = user_id
        self._transport = transport
        self._llm = get_llm_client()
        self._stt = get_stt()
        self._tts = get_tts()
        self._last_event_id: uuid.UUID | None = None

    async def _emit(self, call_id: str, event_type: EventType, payload: dict) -> None:
        self._db.add(CallEvent(call_id=uuid.UUID(call_id), event_type=event_type.value, payload_json=payload))
        await self._db.commit()
        await manager.broadcast(str(self._user_id), event_type, {"call_id": call_id, **payload})

    async def run(self, call_id: str | None = None) -> CallContext:
        call_row = Call(
            id=uuid.UUID(call_id) if call_id and _is_uuid(call_id) else uuid.uuid4(),
            user_id=self._user_id,
            caller_number=self._transport.caller_number,
            status="active",
        )
        self._db.add(call_row)
        await self._db.commit()
        call_id = str(call_row.id)

        context = CallContext(call_id=call_id, user_id=self._user_id, caller_number=self._transport.caller_number)
        await self._emit(call_id, EventType.CALL_INCOMING, {"caller_number": context.caller_number})

        try:
            await self._send_greeting(context)
            while True:
                audio = await self._transport.next_caller_turn()
                if audio is None:
                    break
                await self._handle_caller_turn(call_row, context, audio)
            await self._finish_call(call_row, context)
        except Exception:
            call_row.status = "disconnected"
            call_row.ended_at = datetime.now(timezone.utc)
            await self._db.commit()
            raise
        return context

    async def _send_greeting(self, context: CallContext) -> None:
        call_id = context.call_id
        context.transcript.append(TranscriptTurn(speaker="ai", text=_GREETING, lang="en"))
        self._db.add(CallTranscript(call_id=uuid.UUID(call_id), speaker="ai", text=_GREETING, lang="en"))
        await self._db.commit()
        await self._emit(call_id, EventType.TRANSCRIPT_CHUNK, {"speaker": "ai", "text": _GREETING})

        async def _tts_chunks():
            async for chunk in self._tts.synthesize(_GREETING, "en"):
                yield chunk.data

        await self._transport.send_ai_turn(_tts_chunks())

    async def _handle_caller_turn(self, call_row: Call, context: CallContext, audio: bytes) -> None:
        call_id = context.call_id
        lang = "en"

        async def _one_chunk():
            yield audio

        caller_text = ""
        async for chunk in self._stt.stream_transcribe(_one_chunk(), lang):
            caller_text = chunk.text
        print(f"[pipeline {call_id}] STT: {caller_text!r}", flush=True)

        context.transcript.append(TranscriptTurn(speaker="caller", text=caller_text, lang=lang))
        self._db.add(CallTranscript(call_id=uuid.UUID(call_id), speaker="caller", text=caller_text, lang=lang))
        await self._db.commit()
        await self._emit(call_id, EventType.TRANSCRIPT_CHUNK, {"speaker": "caller", "text": caller_text})

        need_caller_id = context.caller_id_result is None
        caller_id_task = (
            caller_id.identify_caller(self._db, self._llm, self._user_id, context.caller_number, caller_text)
            if need_caller_id
            else None
        )
        intent_task = intent_stage.detect_intent(self._llm, context.transcript_text())
        if caller_id_task is not None:
            result, intent_result = await asyncio.gather(caller_id_task, intent_task)
            context.caller_id_result = result
            call_row.caller_id_result_json = result
            if result.get("contact_id"):
                call_row.contact_id = uuid.UUID(result["contact_id"])
            await self._db.commit()
            await self._emit(call_id, EventType.CALLER_IDENTIFIED, result)
        else:
            intent_result = await intent_task
        context.intent = intent_result
        call_row.intent_json = intent_result
        await self._db.commit()
        await self._emit(call_id, EventType.INTENT_DETECTED, intent_result)
        print(f"[pipeline {call_id}] intent: {intent_result}", flush=True)

        action_summary = await self._maybe_handle_appointment_action(context)

        reply_text = await response_gen.generate_response(self._llm, context, action_summary)
        print(f"[pipeline {call_id}] reply: {reply_text!r}", flush=True)
        context.transcript.append(TranscriptTurn(speaker="ai", text=reply_text, lang=lang))
        self._db.add(CallTranscript(call_id=uuid.UUID(call_id), speaker="ai", text=reply_text, lang=lang))
        await self._db.commit()
        await self._emit(call_id, EventType.TRANSCRIPT_CHUNK, {"speaker": "ai", "text": reply_text})

        async def _tts_chunks():
            async for chunk in self._tts.synthesize(reply_text, lang):
                yield chunk.data

        await self._transport.send_ai_turn(_tts_chunks())
        print(f"[pipeline {call_id}] AI audio sent", flush=True)

    async def _extract_meeting_slot(self, context: CallContext) -> tuple[datetime, datetime] | None:
        now = datetime.now(timezone.utc)
        response = await self._llm.complete(
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Current time: {now.isoformat()}\n"
                        f"Conversation:\n{context.transcript_text()}\n\n"
                        "If the caller and AI agreed on a specific meeting time, extract it. "
                        f"Respond as JSON: {_MEETING_SLOT_SCHEMA}. "
                        "If no specific time was agreed yet, respond with start_at_iso as an empty string."
                    ),
                }
            ],
            system="You extract confirmed meeting times from phone call transcripts.",
            json_schema=_MEETING_SLOT_SCHEMA,
        )
        parsed = response.json or {}
        start_at_iso = parsed.get("start_at_iso") or ""
        if not start_at_iso:
            return None
        try:
            start_at = datetime.fromisoformat(start_at_iso)
        except ValueError:
            return None
        duration = int(parsed.get("duration_minutes") or 45)
        return start_at, start_at + timedelta(minutes=duration)

    async def _maybe_handle_appointment_action(self, context: CallContext) -> str | None:
        intent = context.intent.get("intent") if context.intent else None

        if intent in ("interview", "appointment"):
            slot = await self._extract_meeting_slot(context)
            if slot is None:
                return None
            start_at, end_at = slot
            title = f"{intent.replace('_', ' ').title()} — {context.caller_id_result.get('name') or context.caller_number}"
            decision, event = await create_calendar_event(self._db, context, title, start_at, end_at)
            action = "schedule_meetings"
            ok_summary = f"scheduled '{title}' at {start_at.isoformat()}"
            fail_summary = f"could not schedule meeting: {decision.reason}"
            if event:
                self._last_event_id = uuid.UUID(event["id"])

        elif intent == "reschedule_appointment":
            if self._last_event_id is None:
                return None
            slot = await self._extract_meeting_slot(context)
            if slot is None:
                return None
            start_at, end_at = slot
            decision, event = await reschedule_calendar_event(
                self._db, context, self._last_event_id, start_at, end_at
            )
            action = "schedule_meetings"
            ok_summary = f"rescheduled to {start_at.isoformat()}"
            fail_summary = f"could not reschedule meeting: {decision.reason}"

        elif intent == "cancel_appointment":
            if self._last_event_id is None:
                return None
            decision = await cancel_calendar_event(self._db, context, self._last_event_id)
            # ponytail: no CALENDAR_UPDATED removal event, live dashboard keeps stale
            # entry until next fetch; add a calendar_removed WS event if live removal matters
            event = None
            action = "schedule_meetings"
            ok_summary = "cancelled meeting"
            fail_summary = f"could not cancel meeting: {decision.reason}"
            if decision.allowed:
                self._last_event_id = None

        else:
            return None

        await self._emit(
            context.call_id,
            EventType.ACTION_EXECUTED,
            {"action": action, "allowed": decision.allowed, "reason": decision.reason},
        )
        if not decision.allowed:
            return fail_summary
        if event:
            await self._emit(context.call_id, EventType.CALENDAR_UPDATED, event)
        return ok_summary

    async def _finish_call(self, call_row: Call, context: CallContext) -> None:
        call_row.status = "completed"
        call_row.ended_at = datetime.now(timezone.utc)
        await self._db.commit()

        summary_row = await summary.generate_summary(self._db, self._llm, context)
        await self._emit(
            context.call_id,
            EventType.CALL_SUMMARY_READY,
            {
                "summary": summary_row.summary_text,
                "action_items": summary_row.action_items_json,
                "people": summary_row.people_json,
            },
        )
        await self._transport.end_call()
        await self._emit(context.call_id, EventType.CALL_ENDED, {})


def _is_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False
