from app.config import get_settings
from app.llm.base import LLMClient

settings = get_settings()

_client: LLMClient | None = None


def get_llm_client() -> LLMClient:
    global _client
    if _client is None:
        from app.llm.providers.generic_openai_compatible import GenericOpenAICompatibleClient

        _client = GenericOpenAICompatibleClient(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
            model=settings.LLM_MODEL,
        )
    return _client
