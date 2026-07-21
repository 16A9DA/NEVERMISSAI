"""Mock STT/TTS used for local dev and demos where the real NVIDIA models
(parakeet-1.1b-rnnt-multilingual-asr, chatterbox-multilingual-tts) aren't
available. Selected via STT_PROVIDER=mock / TTS_PROVIDER=mock.

MockSTT does not run real speech recognition: it decodes the incoming
"audio" chunks as UTF-8 text (the mock call transport sends scripted
dialogue lines as bytes in place of a real microphone signal) and, after a
short simulated-latency delay, yields the joined text as the final
transcript. MockTTS returns a short silent audio placeholder instead of
real speech.
"""

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
        text = "".join(chunk.decode("utf-8", errors="ignore") async for chunk in audio_chunks)
        await asyncio.sleep(self._delay_seconds)
        yield TranscriptChunk(text=text, lang=lang, is_final=True)


class MockTTS(TTSProvider):
    """Returns a short silent audio placeholder instead of real speech."""

    async def synthesize(self, text: str, lang: str) -> AsyncIterator[AudioChunk]:
        yield AudioChunk(data=_SILENT_WAV_HEADER, lang=lang)
