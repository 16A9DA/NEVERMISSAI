from abc import ABC, abstractmethod
from collections.abc import AsyncIterator


class CallTransport(ABC):
    caller_number: str

    @abstractmethod
    async def next_caller_turn(self) -> bytes | None: ...

    @abstractmethod
    async def send_ai_turn(self, audio_chunks: AsyncIterator[bytes]) -> None: ...

    @abstractmethod
    async def end_call(self) -> None: ...
