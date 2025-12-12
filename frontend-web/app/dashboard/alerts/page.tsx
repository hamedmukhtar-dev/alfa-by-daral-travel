"use client";

import { useEffect, useState } from "react";
import { api } from "@/app/lib/api";

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<any[]>([]);

  useEffect(() => {
    api.get("/alerts").then((res) => setAlerts(res.data));
  }, []);

  return (
    <main style={{ padding: 24 }}>
      <h1>🚨 التنبيهات</h1>

      <ul>
        {alerts.map((a) => (
          <li key={a.id} style={{ marginBottom: 12 }}>
            <strong>{a.severity.toUpperCase()}</strong> — {a.type}
            <br />
            {a.message}
          </li>
        ))}
      </ul>
    </main>
  );
}
