"""LLM client interface. Every pipeline stage that needs reasoning depends
only on this — never on a vendor SDK directly. Swapping providers is an
LLM_PROVIDER env var change (see app/llm/factory.py).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    text: str
    json: dict | None = None


class LLMClient(ABC):
    @abstractmethod
    async def complete(
        self,
        messages: list[dict[str, str]],
        system: str | None = None,
        json_schema: dict | None = None,
    ) -> LLMResponse:
        """Runs one chat completion. If json_schema is given, the provider
        is expected to return JSON matching it in LLMResponse.json."""
