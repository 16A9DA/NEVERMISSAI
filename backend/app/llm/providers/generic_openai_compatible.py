import json

from openai import AsyncOpenAI

from app.llm.base import LLMClient, LLMResponse


class GenericOpenAICompatibleClient(LLMClient):
    """One adapter over any OpenAI-compatible chat completions endpoint —
    works for OpenAI, OpenRouter, or a local/self-hosted server by pointing
    base_url at it. Which vendor this hits is entirely an env var choice
    (LLM_BASE_URL / LLM_API_KEY / LLM_MODEL), not a code choice.
    """

    def __init__(self, api_key: str, base_url: str, model: str):
        self._client = AsyncOpenAI(api_key=api_key or "unset", base_url=base_url)
        self._model = model

    async def complete(
        self,
        messages: list[dict[str, str]],
        system: str | None = None,
        json_schema: dict | None = None,
    ) -> LLMResponse:
        full_messages = ([{"role": "system", "content": system}] if system else []) + messages
        kwargs = {}
        if json_schema is not None:
            kwargs["response_format"] = {"type": "json_object"}

        completion = await self._client.chat.completions.create(
            model=self._model, messages=full_messages, **kwargs
        )
        text = completion.choices[0].message.content or ""

        parsed = None
        if json_schema is not None:
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                parsed = None

        return LLMResponse(text=text, json=parsed)
