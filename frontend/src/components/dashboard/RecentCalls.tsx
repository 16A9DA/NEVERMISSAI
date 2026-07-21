"use client";

import { useAuth } from "@clerk/nextjs";
import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

interface CallListItem {
  id: string;
  caller_number: string;
  caller_name: string | null;
  status: string;
  started_at: string;
  duration_seconds: number | null;
  intent: string | null;
  summary: string | null;
}

interface CallDetail extends CallListItem {
  transcript: { speaker: string; text: string; ts: string }[];
}

function formatDuration(seconds: number | null) {
  if (seconds === null) return "in progress";
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${s.toString().padStart(2, "0")}`;
}

export function RecentCalls() {
  const { getToken } = useAuth();
  const [calls, setCalls] = useState<CallListItem[]>([]);
  const [selected, setSelected] = useState<CallDetail | null>(null);

  useEffect(() => {
    (async () => {
      const token = await getToken();
      const res = await fetch(`${API_URL}/calls`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      if (res.ok) setCalls(await res.json());
    })();
  }, [getToken]);

  async function openCall(id: string) {
    const token = await getToken();
    const res = await fetch(`${API_URL}/calls/${id}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (res.ok) setSelected(await res.json());
  }

  return (
    <div className="rounded-lg border bg-card p-4">
      <h2 className="text-sm font-medium text-muted-foreground">Recent calls</h2>
      {calls.length === 0 ? (
        <p className="mt-2 text-sm text-muted-foreground">No calls yet.</p>
      ) : (
        <ul className="mt-2 divide-y">
          {calls.map((call) => (
            <li key={call.id}>
              <button
                className="flex w-full items-center justify-between py-2 text-left hover:bg-muted/50"
                onClick={() => openCall(call.id)}
              >
                <span>
                  <span className="font-medium">{call.caller_name || call.caller_number}</span>
                  <span className="ml-2 text-xs text-muted-foreground">{call.intent}</span>
                </span>
                <span className="text-xs text-muted-foreground">{formatDuration(call.duration_seconds)}</span>
              </button>
            </li>
          ))}
        </ul>
      )}

      {selected && (
        <div className="mt-4 rounded-md border p-3">
          <div className="flex items-center justify-between">
            <p className="text-sm font-medium">{selected.caller_name || selected.caller_number}</p>
            <button className="text-xs text-muted-foreground" onClick={() => setSelected(null)}>
              close
            </button>
          </div>
          {selected.summary && <p className="mt-1 text-sm text-muted-foreground">{selected.summary}</p>}
          <div className="mt-2 max-h-64 space-y-1 overflow-y-auto text-sm">
            {selected.transcript.map((turn, i) => (
              <p key={i}>
                <span className="font-medium">{turn.speaker === "ai" ? "Agent" : "Caller"}:</span> {turn.text}
              </p>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
