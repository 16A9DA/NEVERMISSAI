import asyncio
from collections.abc import AsyncIterator

from app.voice.base import AudioChunk, STTProvider, TranscriptChunk, TTSProvider

_SILENT_WAV_HEADER = (
    b"RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00"
    b"\x44\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00"
)


class MockSTT(STTProvider):
    def __init__(self, delay_seconds: float = 0.4):
        self._delay_seconds = delay_seconds

    async def stream_transcribe(
        self, audio_chunks: AsyncIterator[bytes], lang: str
    ) -> AsyncIterator[TranscriptChunk]:
        parts = [chunk.decode("utf-8", errors="ignore") async for chunk in audio_chunks]
        text = "".join(parts)
        await asyncio.sleep(self._delay_seconds)
        yield TranscriptChunk(text=text, lang=lang, is_final=True)


class MockTTS(TTSProvider):
    async def synthesize(self, text: str, lang: str) -> AsyncIterator[AudioChunk]:
        yield AudioChunk(data=_SILENT_WAV_HEADER, lang=lang)
