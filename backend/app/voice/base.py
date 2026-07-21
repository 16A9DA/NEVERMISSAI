"""Speech provider interfaces.

Pipeline code depends only on these ABCs, never on a concrete vendor SDK.
Swapping STT_PROVIDER/TTS_PROVIDER in .env is the entire integration change.
"""

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass


@dataclass
class TranscriptChunk:
    text: str
    lang: str
    is_final: bool


@dataclass
class AudioChunk:
    data: bytes
    lang: str


class STTProvider(ABC):
    @abstractmethod
    async def stream_transcribe(
        self, audio_chunks: AsyncIterator[bytes], lang: str
    ) -> AsyncIterator[TranscriptChunk]:
        """Transcribes a stream of raw audio chunks into transcript chunks."""


class TTSProvider(ABC):
    @abstractmethod
    async def synthesize(self, text: str, lang: str) -> AsyncIterator[AudioChunk]:
        """Synthesizes text into a stream of audio chunks in the given language."""
