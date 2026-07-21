from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy import select

from app.db.models import User
from app.db.session import async_session_maker
from app.deps import get_current_user_id_ws
from app.pipeline.orchestrator import CallPipeline
from app.voice.transport.mock_transport import LiveMockTransport
from app.ws.manager import manager

router = APIRouter()


@router.websocket("/ws/dashboard")
async def dashboard_socket(websocket: WebSocket, user_id: str = Depends(get_current_user_id_ws)):
    await manager.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()  # dashboard is read-only for now, drain keepalives
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)


@router.websocket("/ws/call/{call_id}")
async def call_socket(websocket: WebSocket, call_id: str, clerk_user_id: str = Depends(get_current_user_id_ws)):
    await websocket.accept()
    caller_number = websocket.query_params.get("caller_number", "+10000000000")
    transport = LiveMockTransport(websocket, caller_number)
    async with async_session_maker() as db:
        result = await db.execute(select(User).where(User.clerk_user_id == clerk_user_id))
        user = result.scalar_one_or_none()
        if user is None:
            user = User(clerk_user_id=clerk_user_id)
            db.add(user)
            await db.commit()
            await db.refresh(user)

        pipeline = CallPipeline(db=db, user_id=user.id, transport=transport)
        try:
            await pipeline.run(call_id=call_id)
        except WebSocketDisconnect:
            await transport.end_call()
