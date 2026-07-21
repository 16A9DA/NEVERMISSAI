"use client";

import { useDashboardStore } from "@/lib/store";

export function CalendarWidget() {
  const { calendarEvents } = useDashboardStore();

  return (
    <div className="rounded-xl border border-border bg-card/60 p-4 backdrop-blur">
      <h2 className="mb-3 text-sm font-medium text-muted-foreground">Calendar</h2>
      {calendarEvents.length === 0 ? (
        <p className="text-sm text-muted-foreground">No upcoming events.</p>
      ) : (
        <ul className="space-y-2 text-sm">
          {calendarEvents.map((event) => (
            <li key={event.id} className="rounded-lg bg-muted px-3 py-2">
              <div className="font-medium">{event.title}</div>
              <div className="text-xs text-muted-foreground">
                {new Date(event.start_at).toLocaleString()} — {new Date(event.end_at).toLocaleTimeString()}
              </div>
              {event.location && <div className="text-xs text-muted-foreground">{event.location}</div>}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
