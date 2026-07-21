from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Core services
    DATABASE_URL: str = "postgresql+asyncpg://nevermiss:nevermiss@localhost:5432/nevermiss"
    REDIS_URL: str = "redis://localhost:6379/0"
    CHROMA_URL: str = "http://localhost:8001"

    # LLM (NVIDIA NIM speaks the OpenAI chat completions protocol, so the
    # generic OpenAI-compatible adapter works unchanged against it)
    LLM_PROVIDER: str = "nvidia"
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "meta/llama-3.3-70b-instruct"
    LLM_BASE_URL: str = "https://integrate.api.nvidia.com/v1"

    # Voice
    STT_PROVIDER: Literal["mock", "parakeet"] = "mock"
    TTS_PROVIDER: Literal["mock", "chatterbox"] = "mock"
    SUPPORTED_LANGUAGES: list[str] = ["en", "ar"]

    # Call transport
    CALL_TRANSPORT: Literal["mock", "twilio"] = "mock"
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""

    # Auth
    CLERK_SECRET_KEY: str = ""
    CLERK_JWKS_URL: str = ""

    # App
    ENV: Literal["dev", "prod"] = "dev"


@lru_cache
def get_settings() -> Settings:
    return Settings()
