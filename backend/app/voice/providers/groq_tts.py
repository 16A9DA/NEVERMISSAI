import audioop
import io
import wave
from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from app.config import get_settings
from app.voice.base import AudioChunk, TTSProvider

_VOICE = "hannah"


class GroqTTS(TTSProvider):
    async def synthesize(self, text: str, lang: str) -> AsyncIterator[AudioChunk]:
        settings = get_settings()
        client = AsyncOpenAI(api_key=settings.GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
        response = await client.audio.speech.create(
            model="canopylabs/orpheus-v1-english",
            voice=_VOICE,
            input=text,
            response_format="wav",
        )
        wav_bytes = response.read()

        with wave.open(io.BytesIO(wav_bytes), "rb") as wav_f:
            channels = wav_f.getnchannels()
            sampwidth = wav_f.getsampwidth()
            framerate = wav_f.getframerate()
            pcm = wav_f.readframes(wav_f.getnframes())

        if sampwidth != 2:
            pcm = audioop.lin2lin(pcm, sampwidth, 2)
        if channels == 2:
            pcm = audioop.tomono(pcm, 2, 0.5, 0.5)
        if framerate != 16000:
            pcm, _ = audioop.ratecv(pcm, 2, 1, framerate, 16000, None)

        yield AudioChunk(data=pcm, lang="en")
