"use client";

import { useAuth } from "@clerk/nextjs";
import { useEffect, useState } from "react";
import { useDashboardStore } from "@/lib/store";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export function CalendarWidget() {
  const { calendarEvents } = useDashboardStore();
  const { getToken } = useAuth();
  const [connected, setConnected] = useState<boolean | null>(null);

  useEffect(() => {
    (async () => {
      const token = await getToken();
      const res = await fetch(`${API_URL}/calendar/status`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      if (res.ok) setConnected((await res.json()).connected);
    })();
  }, [getToken]);

  async function connectGoogleCalendar() {
    const token = await getToken();
    window.location.href = `${API_URL}/calendar/connect?token=${encodeURIComponent(token ?? "")}`;
  }

  return (
    <div className="rounded-lg border bg-card p-4">
      <div className="mb-2 flex items-center justify-between">
        <h2 className="text-sm font-medium text-muted-foreground">Google Calendar</h2>
        {connected === false && (
          <button className="text-xs text-primary underline" onClick={connectGoogleCalendar}>
            Connect
          </button>
        )}
      </div>

      {connected === false ? (
        <p className="text-sm text-muted-foreground">Not connected.</p>
      ) : calendarEvents.length === 0 ? (
        <p className="text-sm text-muted-foreground">No upcoming events.</p>
      ) : (
        <ul className="space-y-2 divide-y">
          {calendarEvents.map((event) => (
            <li key={event.id} className="pt-2 text-sm first:pt-0">
              <div className="font-medium">{event.title}</div>
              <div className="text-xs text-muted-foreground">
                {new Date(event.start_at).toLocaleString()} — {new Date(event.end_at).toLocaleTimeString()}
              </div>
              {event.description && <div className="text-xs text-muted-foreground">{event.description}</div>}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
