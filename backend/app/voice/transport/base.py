"""Call transport interface.

The pipeline orchestrator only ever talks to a CallTransport for audio
in/out — it never knows whether the call is a browser tab (mock) or a real
phone line (Twilio). Swapping CALL_TRANSPORT=mock -> CALL_TRANSPORT=twilio
in .env is the entire integration change.

Calls are modeled as a turn-based exchange (caller speaks, AI responds,
repeat) rather than one raw continuous stream, since every pipeline stage
(intent, urgency, scam, permissions, response) operates per-turn.
"""

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator


class CallTransport(ABC):
    caller_number: str

    @abstractmethod
    async def next_caller_turn(self) -> bytes | None:
        """Returns the raw audio for the caller's next utterance, or None
        once the caller has hung up / the call is over."""

    @abstractmethod
    async def send_ai_turn(self, audio_chunks: AsyncIterator[bytes]) -> None:
        """Streams the AI's synthesized reply back to the caller."""

    @abstractmethod
    async def end_call(self) -> None:
        """Terminates the call."""
