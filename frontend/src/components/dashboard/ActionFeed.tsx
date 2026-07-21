"use client";

import { useDashboardStore } from "@/lib/store";

export function ActionFeed() {
  const { actions, summary } = useDashboardStore();

  return (
    <div className="rounded-xl border border-border bg-card/60 p-4 backdrop-blur">
      <h2 className="mb-3 text-sm font-medium text-muted-foreground">Actions</h2>
      {actions.length === 0 ? (
        <p className="text-sm text-muted-foreground">No actions taken yet.</p>
      ) : (
        <ul className="space-y-2 text-sm">
          {actions.map((action, i) => (
            <li key={i} className="flex items-center justify-between">
              <span>{action.action}</span>
              <span className={action.allowed ? "text-green-500" : "text-red-500"}>
                {action.allowed ? "allowed" : "denied"}
              </span>
            </li>
          ))}
        </ul>
      )}
      {summary && (
        <div className="mt-4 border-t border-border pt-3 text-sm text-muted-foreground">
          <span className="mb-1 block font-medium text-foreground">Call summary</span>
          {summary}
        </div>
      )}
    </div>
  );
}
