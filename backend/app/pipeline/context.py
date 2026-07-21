import uuid
from dataclasses import dataclass, field


@dataclass
class TranscriptTurn:
    speaker: str  # "caller" | "ai"
    text: str
    lang: str = "en"


@dataclass
class CallContext:
    call_id: str
    user_id: uuid.UUID
    caller_number: str

    transcript: list[TranscriptTurn] = field(default_factory=list)
    caller_id_result: dict | None = None
    intent: dict | None = None
    urgency_score: int | None = None
    urgency_bucket: str | None = None
    scam_score: int | None = None
    scam_reasons: list[str] = field(default_factory=list)
    memory_hits: list[str] = field(default_factory=list)
    permission_decisions: list[dict] = field(default_factory=list)

    def transcript_text(self) -> str:
        return "\n".join(f"{turn.speaker}: {turn.text}" for turn in self.transcript)
