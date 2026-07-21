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
    ) -> LLMResponse: ...
