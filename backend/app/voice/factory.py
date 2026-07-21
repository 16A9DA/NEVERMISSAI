from app.config import get_settings
from app.voice.base import STTProvider, TTSProvider

settings = get_settings()

_stt: STTProvider | None = None
_tts: TTSProvider | None = None


def get_stt() -> STTProvider:
    global _stt
    if _stt is None:
        if settings.STT_PROVIDER == "mock":
            from app.voice.providers.mock_provider import MockSTT

            _stt = MockSTT()
        else:
            from app.voice.providers.parakeet_stt import ParakeetSTT

            _stt = ParakeetSTT()
    return _stt


def get_tts() -> TTSProvider:
    global _tts
    if _tts is None:
        if settings.TTS_PROVIDER == "mock":
            from app.voice.providers.mock_provider import MockTTS

            _tts = MockTTS()
        else:
            from app.voice.providers.chatterbox_tts import ChatterboxTTS

            _tts = ChatterboxTTS()
    return _tts
