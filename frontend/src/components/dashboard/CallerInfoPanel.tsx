"use client";

import { useDashboardStore } from "@/lib/store";

export function CallerInfoPanel() {
  const { callerId, intent } = useDashboardStore();

  return (
    <div className="rounded-xl border border-border bg-card/60 p-4 backdrop-blur">
      <h2 className="mb-3 text-sm font-medium text-muted-foreground">Caller information</h2>
      {!callerId ? (
        <p className="text-sm text-muted-foreground">Waiting for a call.</p>
      ) : (
        <div className="space-y-2 text-sm">
          <div className="flex items-center justify-between">
            <span className="font-medium capitalize">{callerId.relation_type}</span>
            <span className="text-xs text-muted-foreground">
              {Math.round(callerId.confidence * 100)}% confidence
            </span>
          </div>
          {callerId.name && <p className="text-muted-foreground">{callerId.name}</p>}
          {intent && <p className="text-muted-foreground">Intent: {intent.intent}</p>}
        </div>
      )}
    </div>
  );
}
