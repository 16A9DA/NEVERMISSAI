import json
import traceback

from fastapi import APIRouter, Depends, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db.models import User
from app.deps import get_call_owner, get_db
from app.pipeline.orchestrator import CallPipeline
from app.voice.transport.twilio_transport import TwilioTransport

router = APIRouter(prefix="/twilio", tags=["twilio"])


@router.post("/voice")
async def voice_webhook(From: str = Form(...)):
    settings = get_settings()
    ws_url = settings.PUBLIC_BASE_URL.replace("https://", "wss://").replace("http://", "ws://")
    twiml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        "<Response><Connect><Stream url=\"{ws_url}/twilio/media\">"
        '<Parameter name="caller" value="{caller}"/>'
        "</Stream></Connect></Response>"
    ).format(ws_url=ws_url, caller=From)
    return Response(content=twiml, media_type="application/xml")


@router.websocket("/media")
async def media_stream(
    websocket: WebSocket,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_call_owner),
):
    await websocket.accept()

    stream_sid = None
    caller_number = "unknown"
    while stream_sid is None:
        message = await websocket.receive_text()
        frame = json.loads(message)
        if frame.get("event") == "start":
            stream_sid = frame["start"]["streamSid"]
            caller_number = frame["start"].get("customParameters", {}).get("caller", "unknown")

    transport = TwilioTransport(websocket=websocket, caller_number=caller_number, stream_sid=stream_sid)
    pipeline = CallPipeline(db=db, user_id=user.id, transport=transport)
    try:
        await pipeline.run()
    except WebSocketDisconnect:
        print(f"[twilio] call {stream_sid} ended: caller hung up", flush=True)
    except Exception as e:
        print(f"[twilio] call {stream_sid} crashed: {e!r}\n{traceback.format_exc()}", flush=True)
    finally:
        try:
            await websocket.close()
        except RuntimeError:
            pass
