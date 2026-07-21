import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Call, CallSummary, CallTranscript, User
from app.deps import get_current_user, get_db

router = APIRouter(prefix="/calls", tags=["calls"])


def _duration_seconds(call: Call) -> int | None:
    if call.ended_at is None:
        return None
    return int((call.ended_at - call.started_at).total_seconds())


@router.get("")
async def list_calls(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Call, CallSummary.summary_text)
        .outerjoin(CallSummary, CallSummary.call_id == Call.id)
        .where(Call.user_id == user.id)
        .order_by(Call.started_at.desc())
    )
    return [
        {
            "id": str(call.id),
            "caller_number": call.caller_number,
            "caller_name": (call.caller_id_result_json or {}).get("name"),
            "status": call.status,
            "started_at": call.started_at.isoformat(),
            "ended_at": call.ended_at.isoformat() if call.ended_at else None,
            "duration_seconds": _duration_seconds(call),
            "intent": (call.intent_json or {}).get("intent"),
            "summary": summary_text,
        }
        for call, summary_text in result.all()
    ]


@router.get("/{call_id}")
async def get_call(
    call_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    call = (
        await db.execute(select(Call).where(Call.id == call_id, Call.user_id == user.id))
    ).scalar_one_or_none()
    if call is None:
        raise HTTPException(404, "call not found")

    transcript = (
        await db.execute(
            select(CallTranscript).where(CallTranscript.call_id == call_id).order_by(CallTranscript.ts)
        )
    ).scalars().all()
    summary_row = (
        await db.execute(select(CallSummary).where(CallSummary.call_id == call_id))
    ).scalar_one_or_none()

    return {
        "id": str(call.id),
        "caller_number": call.caller_number,
        "caller_name": (call.caller_id_result_json or {}).get("name"),
        "status": call.status,
        "started_at": call.started_at.isoformat(),
        "ended_at": call.ended_at.isoformat() if call.ended_at else None,
        "duration_seconds": _duration_seconds(call),
        "intent": call.intent_json,
        "transcript": [
            {"speaker": turn.speaker, "text": turn.text, "ts": turn.ts.isoformat()} for turn in transcript
        ],
        "summary": summary_row.summary_text if summary_row else None,
        "action_items": summary_row.action_items_json if summary_row else None,
    }
