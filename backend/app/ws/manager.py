import json
from collections import defaultdict
from typing import Any

from fastapi import WebSocket

from app.ws.events import EventType


class ConnectionManager:
    def __init__(self):
        self._connections: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, user_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections[user_id].add(websocket)

    def disconnect(self, user_id: str, websocket: WebSocket) -> None:
        self._connections[user_id].discard(websocket)

    async def broadcast(self, user_id: str, event_type: EventType, payload: dict[str, Any]) -> None:
        message = json.dumps({"type": event_type.value, "payload": payload}, default=str)
        dead: list[WebSocket] = []
        for ws in self._connections.get(user_id, set()):
            try:
                await ws.send_text(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(user_id, ws)


manager = ConnectionManager()
