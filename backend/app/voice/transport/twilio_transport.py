import asyncio
import audioop
import base64
import json

from fastapi import WebSocket

from app.voice.transport.base import CallTransport

_SILENCE_RMS_THRESHOLD = 25
_SILENCE_FRAMES_TO_END_TURN = 60
_MIN_SPEECH_FRAMES = 5


class TwilioTransport(CallTransport):
    def __init__(self, websocket: WebSocket, caller_number: str, stream_sid: str):
        self._ws = websocket
        self.caller_number = caller_number
        self._stream_sid = stream_sid
        self._ended = False

    async def next_caller_turn(self) -> bytes | None:
        if self._ended:
            return None

        speech_pcm8k = bytearray()
        silence_run = 0
        speech_frames = 0

        while True:
            message = await self._ws.receive_text()
            frame = json.loads(message)
            event = frame.get("event")

            if event == "stop":
                self._ended = True
                return bytes(speech_pcm8k) if speech_frames >= _MIN_SPEECH_FRAMES else None

            if event != "media":
                continue

            mulaw = base64.b64decode(frame["media"]["payload"])
            pcm8k = audioop.ulaw2lin(mulaw, 2)
            rms = audioop.rms(pcm8k, 2)

            if rms >= _SILENCE_RMS_THRESHOLD:
                speech_pcm8k += pcm8k
                speech_frames += 1
                silence_run = 0
            elif speech_frames > 0:
                speech_pcm8k += pcm8k
                silence_run += 1
                if silence_run >= _SILENCE_FRAMES_TO_END_TURN:
                    if speech_frames >= _MIN_SPEECH_FRAMES:
                        return _upsample_to_16k(bytes(speech_pcm8k))
                    speech_pcm8k = bytearray()
                    speech_frames = 0
                    silence_run = 0

    async def send_ai_turn(self, audio_chunks) -> None:
        pcm16k = bytearray()
        async for chunk in audio_chunks:
            pcm16k += chunk
        if not pcm16k:
            return

        drain_task = asyncio.create_task(self._drain_while_sending())

        mulaw8k = _downsample_to_8k_mulaw(bytes(pcm16k))
        frame_size = 160
        for i in range(0, len(mulaw8k), frame_size):
            payload = base64.b64encode(mulaw8k[i : i + frame_size]).decode("ascii")
            await self._ws.send_text(
                json.dumps({"event": "media", "streamSid": self._stream_sid, "media": {"payload": payload}})
            )

        drain_task.cancel()

    async def _drain_while_sending(self) -> None:
        while True:
            message = await self._ws.receive_text()
            if json.loads(message).get("event") == "stop":
                self._ended = True
                return

    async def end_call(self) -> None:
        self._ended = True


def _upsample_to_16k(pcm8k: bytes) -> bytes:
    converted, _ = audioop.ratecv(pcm8k, 2, 1, 8000, 16000, None)
    return converted


def _downsample_to_8k_mulaw(pcm16k: bytes) -> bytes:
    pcm8k, _ = audioop.ratecv(pcm16k, 2, 1, 16000, 8000, None)
    return audioop.lin2ulaw(pcm8k, 2)
