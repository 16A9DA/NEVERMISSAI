from app.config import get_settings
from app.voice.base import STTProvider, TTSProvider

settings = get_settings()

_stt: STTProvider | None = None
_tts: TTSProvider | None = None


def get_stt() -> STTProvider:
    global _stt
    if _stt is None:
        if settings.STT_PROVIDER == "groq":
            from app.voice.providers.groq_stt import GroqSTT

            _stt = GroqSTT()
        else:
            from app.voice.providers.mock_provider import MockSTT

            _stt = MockSTT()
    return _stt


def get_tts() -> TTSProvider:
    global _tts
    if _tts is None:
        if settings.TTS_PROVIDER == "groq":
            from app.voice.providers.groq_tts import GroqTTS

            _tts = GroqTTS()
        else:
            from app.voice.providers.mock_provider import MockTTS

            _tts = MockTTS()
    return _tts
