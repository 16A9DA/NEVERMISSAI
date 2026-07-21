from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.deps import get_current_user_id_ws
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
