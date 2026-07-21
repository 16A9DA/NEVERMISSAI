"""Mock call transports — the primary demo path (no Twilio/phone line
needed). Two flavors:

- ScriptedMockTransport: plays a fixed list of caller lines with no
  browser involved, used by POST /demo/place-call (the presentation
  safety net).
- LiveMockTransport: bridges a browser tab connected to /ws/call/{id} as
  the "phone line" — the caller types (or, later, speaks) a line, the
  server runs it through the pipeline and replies.

Both feed MockSTT/MockTTS via UTF-8-encoded text standing in for real
audio (see app/voice/providers/mock_provider.py) since no real ASR/TTS
models are wired up yet.
"""

from collections.abc import AsyncIterator

from fastapi import WebSocket

from app.voice.transport.base import CallTransport

# Scripted caller lines for the four demo scenarios (POST /demo/place-call).
DEMO_SCRIPTS: dict[str, list[str]] = {
    "recruiter": [
        "Hi, this is Jordan from Acme Talent Partners, I'm calling about the "
        "senior engineer role — is now a good time to find an interview slot?",
        "Great, does sometime Thursday afternoon work for a 45 minute interview?",
        "Perfect, Thursday 2pm works on our end too. I'll send a calendar invite.",
        "Thanks so much, talk soon!",
    ],
    "delivery": [
        "Hey, this is your delivery driver, I'm outside with your package, "
        "where would you like me to leave it?",
        "Got it, leaving it by the side door. Have a good one.",
    ],
    "scam": [
        "This is an urgent security alert from your bank, we've detected "
        "suspicious activity, can you confirm your one-time passcode to verify your identity?",
        "I understand your concern, but I need that code right now or your account will be locked.",
    ],
    "hospital": [
        "This is Saint Mary's Hospital calling, there's been an accident "
        "and we need to reach a family member immediately.",
    ],
}


class ScriptedMockTransport(CallTransport):
    def __init__(self, caller_number: str, script: list[str]):
        self.caller_number = caller_number
        self._script = list(script)
        self._index = 0

    async def next_caller_turn(self) -> bytes | None:
        if self._index >= len(self._script):
            return None
        line = self._script[self._index]
        self._index += 1
        return line.encode("utf-8")

    async def send_ai_turn(self, audio_chunks: AsyncIterator[bytes]) -> None:
        async for _ in audio_chunks:
            pass  # scripted demo has no listener, audio is discarded

    async def end_call(self) -> None:
        self._index = len(self._script)


class LiveMockTransport(CallTransport):
    """Turn-based text bridge over a browser WebSocket at /ws/call/{id}.

    Expects the browser to send `{"text": "..."}` per caller turn and
    `{"end": true}` to hang up. The AI's reply (text + pipeline events) is
    not echoed back on this socket — it is broadcast on /ws/dashboard like
    every other call, which is what the dashboard UI watches.
    """

    def __init__(self, websocket: WebSocket, caller_number: str):
        self._ws = websocket
        self.caller_number = caller_number
        self._ended = False

    async def next_caller_turn(self) -> bytes | None:
        if self._ended:
            return None
        message = await self._ws.receive_json()
        if message.get("end"):
            self._ended = True
            return None
        return str(message.get("text", "")).encode("utf-8")

    async def send_ai_turn(self, audio_chunks: AsyncIterator[bytes]) -> None:
        async for _ in audio_chunks:
            pass  # placeholder audio isn't played in the browser demo client

    async def end_call(self) -> None:
        self._ended = True
