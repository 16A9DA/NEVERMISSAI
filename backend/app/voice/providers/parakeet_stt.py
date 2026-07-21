"""Real STT via NVIDIA parakeet-1.1b-rnnt-multilingual-asr.

Not wired up yet (Phase 6 per the build plan) — this is the seam where a
NeMo/Riva client integration goes once the model is available on the demo
machine. Selected via STT_PROVIDER=parakeet.
"""

from collections.abc import AsyncIterator

from app.voice.base import STTProvider, TranscriptChunk


class ParakeetSTT(STTProvider):
    async def stream_transcribe(
        self, audio_chunks: AsyncIterator[bytes], lang: str
    ) -> AsyncIterator[TranscriptChunk]:
        raise NotImplementedError(
            "parakeet-1.1b-rnnt-multilingual-asr integration not implemented yet; "
            "set STT_PROVIDER=mock for local dev/demo"
        )
        yield  # pragma: no cover - keeps this an async generator
