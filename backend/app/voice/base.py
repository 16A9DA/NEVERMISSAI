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
    ) -> AsyncIterator[TranscriptChunk]: ...


class TTSProvider(ABC):
    @abstractmethod
    async def synthesize(self, text: str, lang: str) -> AsyncIterator[AudioChunk]: ...
