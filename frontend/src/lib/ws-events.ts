// Mirrors backend/app/ws/events.py — keep both in sync by hand for now.
export type EventType =
  | "call_incoming"
  | "transcript_chunk"
  | "caller_identified"
  | "intent_detected"
  | "urgency_updated"
  | "scam_score_updated"
  | "memory_lookup"
  | "action_executed"
  | "calendar_updated"
  | "emergency_alert"
  | "call_summary_ready"
  | "call_ended";

export interface DashboardEvent {
  type: EventType;
  payload: Record<string, unknown> & { call_id: string };
}

export interface TranscriptEntry {
  speaker: "caller" | "ai";
  text: string;
}

export interface CallerIdResult {
  relation_type: string;
  name: string | null;
  confidence: number;
  source: string;
}

export interface IntentResult {
  intent: string;
  confidence: number;
}

export interface ActionEvent {
  action: string;
  allowed: boolean;
  reason: string;
}

export interface CalendarEventPayload {
  id: string;
  title: string;
  start_at: string;
  end_at: string;
  location: string | null;
}
