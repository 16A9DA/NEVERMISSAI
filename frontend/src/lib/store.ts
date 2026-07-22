// Tiny vanilla store (subscribe/getSnapshot) instead of pulling in a state
// library — one dashboard page consumes this, React's built-in
// useSyncExternalStore is all the ceremony it needs.
import { useSyncExternalStore } from "react";
import type {
  ActionEvent,
  CalendarEventPayload,
  CallerIdResult,
  DashboardEvent,
  IntentResult,
  TranscriptEntry,
} from "./ws-events";

export interface DashboardState {
  connected: boolean;
  activeCallId: string | null;
  transcript: TranscriptEntry[];
  callerId: CallerIdResult | null;
  intent: IntentResult | null;
  actions: ActionEvent[];
  calendarEvents: CalendarEventPayload[];
  summary: string | null;
  callListVersion: number;
}

const initialState: DashboardState = {
  connected: false,
  activeCallId: null,
  transcript: [],
  callerId: null,
  intent: null,
  actions: [],
  calendarEvents: [],
  summary: null,
  callListVersion: 0,
};

let state: DashboardState = initialState;
const listeners = new Set<() => void>();

function setState(patch: Partial<DashboardState>) {
  state = { ...state, ...patch };
  listeners.forEach((listener) => listener());
}

export function resetDashboardStore() {
  state = initialState;
  listeners.forEach((listener) => listener());
}

export function applyDashboardEvent(event: DashboardEvent) {
  const { type, payload } = event;
  switch (type) {
    case "call_incoming":
      setState({
        activeCallId: payload.call_id,
        transcript: [],
        callerId: null,
        intent: null,
        actions: [],
        summary: null,
        callListVersion: state.callListVersion + 1,
      });
      break;
    case "transcript_chunk":
      setState({
        transcript: [
          ...state.transcript,
          { speaker: payload.speaker as "caller" | "ai", text: payload.text as string },
        ],
      });
      break;
    case "caller_identified":
      setState({ callerId: payload as unknown as CallerIdResult });
      break;
    case "intent_detected":
      setState({ intent: payload as unknown as IntentResult });
      break;
    case "action_executed":
      setState({ actions: [...state.actions, payload as unknown as ActionEvent] });
      break;
    case "calendar_updated": {
      const incoming = payload as unknown as CalendarEventPayload;
      const withoutDupe = state.calendarEvents.filter((event) => event.id !== incoming.id);
      setState({ calendarEvents: [...withoutDupe, incoming] });
      break;
    }
    case "call_summary_ready":
      setState({ summary: payload.summary as string });
      break;
    case "call_ended":
      setState({ callListVersion: state.callListVersion + 1 });
      break;
    default:
      break;
  }
}

export function setConnected(connected: boolean) {
  setState({ connected });
}

export function setCalendarEvents(events: CalendarEventPayload[]) {
  setState({ calendarEvents: events });
}

function subscribe(listener: () => void) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

function getSnapshot() {
  return state;
}

export function useDashboardStore(): DashboardState {
  return useSyncExternalStore(subscribe, getSnapshot, () => initialState);
}
