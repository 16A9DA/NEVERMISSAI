from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "postgresql+asyncpg://nevermiss:nevermiss@localhost:5432/nevermiss"
    REDIS_URL: str = "redis://localhost:6379/0"
    CHROMA_URL: str = "http://localhost:8001"

    LLM_PROVIDER: str = "groq"
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "llama-3.3-70b-versatile"
    LLM_BASE_URL: str = "https://api.groq.com/openai/v1"

    STT_PROVIDER: Literal["mock", "groq"] = "mock"
    TTS_PROVIDER: Literal["mock", "groq"] = "mock"
    GROQ_API_KEY: str = ""
    SUPPORTED_LANGUAGES: list[str] = ["en", "ar"]
    DEFAULT_LANGUAGE: Literal["en", "ar"] = "en"
    LANGUAGE_DETECTION: bool = True

    CALL_TRANSPORT: Literal["mock", "twilio"] = "mock"
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    PUBLIC_BASE_URL: str = ""

    CLERK_SECRET_KEY: str = ""
    CLERK_JWKS_URL: str = ""

    ENV: Literal["dev", "prod"] = "dev"


@lru_cache
def get_settings() -> Settings:
    return Settings()
