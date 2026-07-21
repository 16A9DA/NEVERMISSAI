import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.deps import get_current_user, get_db
from app.pipeline.orchestrator import CallPipeline
from app.voice.transport.mock_transport import DEMO_SCRIPTS, ScriptedMockTransport

router = APIRouter(prefix="/demo", tags=["demo"])

_DEMO_CALLER_NUMBERS = {
    "recruiter": "+15550100001",
    "delivery": "+15550100002",
    "scam": "+15559990000",
    "hospital": "+15550100003",
}


class PlaceCallRequest(BaseModel):
    scenario: str


@router.post("/place-call")
async def place_call(
    body: PlaceCallRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Runs a scripted demo call end-to-end through the real pipeline —
    the presentation safety net if a live mic demo has AV problems."""
    if body.scenario not in DEMO_SCRIPTS:
        raise HTTPException(400, f"unknown scenario '{body.scenario}', choose one of {list(DEMO_SCRIPTS)}")

    caller_number = _DEMO_CALLER_NUMBERS[body.scenario]
    transport = ScriptedMockTransport(caller_number=caller_number, script=DEMO_SCRIPTS[body.scenario])
    pipeline = CallPipeline(db=db, user_id=user.id, transport=transport)
    call_id = str(uuid.uuid4())
    context = await pipeline.run(call_id=call_id)

    return {
        "call_id": context.call_id,
        "caller_id_result": context.caller_id_result,
        "intent": context.intent,
        "transcript": [vars(turn) for turn in context.transcript],
    }
