"""Real TTS via NVIDIA chatterbox-multilingual-tts.

Not wired up yet (Phase 6 per the build plan) — this is the seam for a
real synthesis client once the model is available on the demo machine.
Selected via TTS_PROVIDER=chatterbox.
"""

from collections.abc import AsyncIterator

from app.voice.base import AudioChunk, TTSProvider


class ChatterboxTTS(TTSProvider):
    async def synthesize(self, text: str, lang: str) -> AsyncIterator[AudioChunk]:
        raise NotImplementedError(
            "chatterbox-multilingual-tts integration not implemented yet; "
            "set TTS_PROVIDER=mock for local dev/demo"
        )
        yield  # pragma: no cover - keeps this an async generator
