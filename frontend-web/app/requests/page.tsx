"use client";

import { useEffect, useState } from "react";
import { api } from "@/app/lib/api";
import IntentBadge from "@/app/components/IntentBadge";

type Request = {
  id: number;
  title: string;
  category: string;
  user_phone: string;
  city_from?: string;
  city_to?: string;
  price_offer?: number;
  intent_score: "high" | "medium" | "low";
  status: string;
};

const order: Record<string, number> = {
  high: 1,
  medium: 2,
  low: 3,
};

export default function RequestsPage() {
  const [requests, setRequests] = useState<Request[]>([]);
  const [filter, setFilter] = useState<"" | "high" | "medium" | "low">("");

  useEffect(() => {
    api.get("/requests").then((res) => {
      const sorted = res.data.sort(
        (a: Request, b: Request) =>
          order[a.intent_score] - order[b.intent_score]
      );
      setRequests(sorted);
    });
  }, []);

  const visible = filter
    ? requests.filter((r) => r.intent_score === filter)
    : requests;

  return (
    <main style={{ padding: 20 }}>
      <h1>طلبات الخدمات</h1>

      {/* Filters */}
      <div style={{ marginBottom: 16 }}>
        <button onClick={() => setFilter("")}>الكل</button>{" "}
        <button onClick={() => setFilter("high")}>🔴 الجادة</button>{" "}
        <button onClick={() => setFilter("medium")}>🟡 المتوسطة</button>{" "}
        <button onClick={() => setFilter("low")}>⚪ استفسارات</button>
      </div>

      {visible.length === 0 && <p>لا توجد طلبات</p>}

      {visible.map((r) => (
        <div
          key={r.id}
          style={{
            border: "1px solid #ddd",
            padding: 12,
            marginBottom: 10,
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
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

          <div style={{ fontSize: 12, color: "#777" }}>
            الحالة: {r.status}
          </div>
        </div>
      ))}
    </main>
  );
}
