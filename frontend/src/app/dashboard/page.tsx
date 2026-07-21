"use client";

import { useAuth } from "@clerk/nextjs";
import { useEffect } from "react";
import { ActionFeed } from "@/components/dashboard/ActionFeed";
import { CalendarWidget } from "@/components/dashboard/CalendarWidget";
import { CallerInfoPanel } from "@/components/dashboard/CallerInfoPanel";
import { RecentCalls } from "@/components/dashboard/RecentCalls";
import { StatusCard } from "@/components/dashboard/StatusCard";
import { TranscriptStream } from "@/components/dashboard/TranscriptStream";
import { useDashboardSocket } from "@/hooks/useDashboardSocket";
import { setCalendarEvents } from "@/lib/store";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function DashboardPage() {
  useDashboardSocket();
  const { getToken } = useAuth();

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

  return (
    <div className="space-y-6">
      <StatusCard />

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <div className="space-y-4">
          <TranscriptStream />
          <RecentCalls />
        </div>
        <div className="space-y-4">
          <CallerInfoPanel />
          <ActionFeed />
          <CalendarWidget />
        </div>
      </div>
    </div>
  );
}
