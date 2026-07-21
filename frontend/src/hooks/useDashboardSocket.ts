"use client";

import { useAuth } from "@clerk/nextjs";
import { useEffect } from "react";
import { applyDashboardEvent, setConnected } from "@/lib/store";
import type { DashboardEvent } from "@/lib/ws-events";

const WS_URL = process.env.NEXT_PUBLIC_WS_URL ?? "ws://localhost:8000";

export function useDashboardSocket() {
  const { getToken } = useAuth();

  useEffect(() => {
    let socket: WebSocket | null = null;
    let cancelled = false;

    (async () => {
      const token = await getToken();
      if (cancelled) return;
      socket = new WebSocket(`${WS_URL}/ws/dashboard?token=${encodeURIComponent(token ?? "")}`);
      socket.onopen = () => setConnected(true);
      socket.onclose = () => setConnected(false);
      socket.onmessage = (event) => {
        try {
          applyDashboardEvent(JSON.parse(event.data) as DashboardEvent);
        } catch {
          // ignore malformed frames
        }
      };
    })();

    return () => {
      cancelled = true;
      socket?.close();
    };
  }, [getToken]);
}
