"use client";

import { useAuth } from "@clerk/nextjs";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { ActionFeed } from "@/components/dashboard/ActionFeed";
import { CalendarWidget } from "@/components/dashboard/CalendarWidget";
import { CallerInfoPanel } from "@/components/dashboard/CallerInfoPanel";
import { TranscriptStream } from "@/components/dashboard/TranscriptStream";
import { useDashboardSocket } from "@/hooks/useDashboardSocket";
import { setCalendarEvents } from "@/lib/store";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const SCENARIOS = ["recruiter", "delivery", "scam", "hospital"] as const;

export default function DashboardPage() {
  useDashboardSocket();
  const { getToken } = useAuth();
  const [placing, setPlacing] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      const token = await getToken();
      const res = await fetch(`${API_URL}/calendar/events`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      if (res.ok) {
        setCalendarEvents(await res.json());
      }
    })();
  }, [getToken]);

  async function placeCall(scenario: string) {
    setPlacing(scenario);
    try {
      const token = await getToken();
      await fetch(`${API_URL}/demo/place-call`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ scenario }),
      });
    } finally {
      setPlacing(null);
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Live dashboard</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Trigger a scripted demo call and watch the pipeline run live below.
        </p>
        <div className="mt-4 flex flex-wrap gap-2">
          {SCENARIOS.map((scenario) => (
            <Button key={scenario} variant="outline" disabled={placing !== null} onClick={() => placeCall(scenario)}>
              {placing === scenario ? "Calling…" : `Place ${scenario} call`}
            </Button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <TranscriptStream />
        <div className="space-y-4">
          <CallerInfoPanel />
          <ActionFeed />
          <CalendarWidget />
        </div>
      </div>
    </div>
  );
}
