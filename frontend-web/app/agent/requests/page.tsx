"use client";

import { useEffect, useState } from "react";
import { api } from "@/app/lib/api";
import IntentBadge from "@/app/components/IntentBadge";

type AgentRequest = {
  id: number;
  title: string;
  category: string;
  city_from?: string;
  city_to?: string;
  price_offer?: number;
  intent_score: "high" | "medium";
};

export default function AgentRequestsPage() {
  const [requests, setRequests] = useState<AgentRequest[]>([]);

  const load = () => {
    api.get("/agent/requests").then((res) => setRequests(res.data));
  };

  useEffect(() => {
    load();
  }, []);

  const claim = async (id: number) => {
    await api.post(`/agent/claim/${id}`);
    alert("تم حجز الطلب لك مؤقتًا");
    load();
  };

  return (
    <main style={{ padding: 20 }}>
      <h1>طلبات جاهزة للتنفيذ</h1>

      {requests.length === 0 && <p>لا توجد طلبات حالياً</p>}

      {requests.map((r) => (
        <div
          key={r.id}
          style={{
            border: "1px solid #ddd",
            padding: 12,
            marginBottom: 10,
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <strong>{r.title}</strong>
            <IntentBadge score={r.intent_score} />
          </div>

          <div style={{ fontSize: 13, color: "#555" }}>
            {r.category} — {r.city_from} {r.city_to && `→ ${r.city_to}`}
          </div>

          {r.price_offer && (
            <div style={{ fontSize: 13 }}>
              الميزانية: {r.price_offer}
            </div>
          )}

          <button
            style={{ marginTop: 8 }}
            onClick={() => claim(r.id)}
          >
            Claim الطلب
          </button>
        </div>
      ))}
    </main>
  );
}
