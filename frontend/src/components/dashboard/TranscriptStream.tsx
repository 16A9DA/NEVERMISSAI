"use client";

import { useDashboardStore } from "@/lib/store";

export function TranscriptStream() {
  const { transcript, connected } = useDashboardStore();

  return (
    <div className="rounded-xl border border-border bg-card/60 p-4 backdrop-blur">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-sm font-medium text-muted-foreground">Conversation transcript</h2>
        <span className={connected ? "text-xs text-green-500" : "text-xs text-muted-foreground"}>
          {connected ? "live" : "disconnected"}
        </span>
      </div>
      {transcript.length === 0 ? (
        <p className="text-sm text-muted-foreground">No active call.</p>
      ) : (
        <div className="flex max-h-80 flex-col gap-2 overflow-y-auto">
          {transcript.map((turn, i) => (
            <div
              key={i}
              className={
                turn.speaker === "ai"
                  ? "self-end rounded-lg bg-primary/10 px-3 py-2 text-sm"
                  : "self-start rounded-lg bg-muted px-3 py-2 text-sm"
              }
            >
              <span className="mr-2 text-xs uppercase text-muted-foreground">{turn.speaker}</span>
              {turn.text}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
