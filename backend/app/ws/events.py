from enum import StrEnum


class EventType(StrEnum):
    CALL_INCOMING = "call_incoming"
    TRANSCRIPT_CHUNK = "transcript_chunk"
    CALLER_IDENTIFIED = "caller_identified"
    INTENT_DETECTED = "intent_detected"
    URGENCY_UPDATED = "urgency_updated"
    SCAM_SCORE_UPDATED = "scam_score_updated"
    MEMORY_LOOKUP = "memory_lookup"
    ACTION_EXECUTED = "action_executed"
    CALENDAR_UPDATED = "calendar_updated"
    EMERGENCY_ALERT = "emergency_alert"
    CALL_SUMMARY_READY = "call_summary_ready"
    CALL_ENDED = "call_ended"
