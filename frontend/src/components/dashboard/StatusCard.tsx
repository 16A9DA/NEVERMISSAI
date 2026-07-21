"use client";

import { useEffect, useState } from "react";
import { useDashboardStore } from "@/lib/store";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export function StatusCard() {
  const { connected } = useDashboardStore();
  const [phoneNumber, setPhoneNumber] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      const res = await fetch(`${API_URL}/health`);
      if (res.ok) {
        const data = await res.json();
        setPhoneNumber(data.phone_number || null);
      }
    })();
  }, []);

  return (
    <div className="rounded-lg border bg-card p-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-muted-foreground">Agent phone number</p>
          <p className="text-lg font-semibold">{phoneNumber || "Not configured"}</p>
        </div>
        <div className="flex items-center gap-2">
          <span className={`h-2.5 w-2.5 rounded-full ${connected ? "bg-green-500" : "bg-gray-400"}`} />
          <span className="text-sm text-muted-foreground">{connected ? "Online" : "Offline"}</span>
        </div>
      </div>
    </div>
  );
}
