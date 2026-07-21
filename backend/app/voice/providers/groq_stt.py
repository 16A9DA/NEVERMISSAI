import io
import wave
from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from app.config import get_settings
from app.voice.base import STTProvider, TranscriptChunk


class GroqSTT(STTProvider):
    async def stream_transcribe(
        self, audio_chunks: AsyncIterator[bytes], lang: str
    ) -> AsyncIterator[TranscriptChunk]:
        parts = [chunk async for chunk in audio_chunks]
        pcm16k = b"".join(parts)

        wav_buf = io.BytesIO()
        with wave.open(wav_buf, "wb") as wav_f:
            wav_f.setnchannels(1)
            wav_f.setsampwidth(2)
            wav_f.setframerate(16000)
            wav_f.writeframes(pcm16k)

        settings = get_settings()
        client = AsyncOpenAI(api_key=settings.GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
        response = await client.audio.transcriptions.create(
            model="whisper-large-v3-turbo",
            file=("audio.wav", wav_buf.getvalue(), "audio/wav"),
            language="en",
            prompt="Phone call about scheduling a business appointment. Times mentioned may include 2 p.m., 4 p.m., 10 a.m.",
        )
        yield TranscriptChunk(text=response.text.strip(), lang="en", is_final=True)
