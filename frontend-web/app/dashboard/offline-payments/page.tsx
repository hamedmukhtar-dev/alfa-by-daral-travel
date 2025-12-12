"use client";

import { useEffect, useState } from "react";
import { api } from "@/app/lib/api";
import ConfirmAction from "@/app/components/ConfirmAction";

type Payment = {
  id: number;
  user_id: number;
  amount: number;
  method: string;
  status: string;
};

export default function OfflinePaymentsPage() {
  const [payments, setPayments] = useState<Payment[]>([]);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const res = await api.get("/admin/offline-payments");
      setPayments(res.data);
    } catch {
      alert("Failed to load offline payments");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const approve = async (id: number) => {
    await api.post("/offline-payments/admin/approve", {
      payment_id: id,
    });
    await load();
  };

  const reject = async (id: number) => {
    await api.post("/offline-payments/admin/reject", {
      payment_id: id,
      reason: "Rejected by admin",
    });
    await load();
  };

  if (loading) return <div style={{ padding: 20 }}>Loading…</div>;

  return (
    <div style={{ padding: 20 }}>
      <h2 style={{ marginBottom: 12 }}>Offline Payments</h2>

      {payments.length === 0 && <p>No payments</p>}

      {payments.map((p) => (
        <div
          key={p.id}
          style={{
            border: "1px solid #ddd",
            padding: 12,
            marginBottom: 8,
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <div>
            <strong>#{p.id}</strong> — User {p.user_id}
            <div style={{ fontSize: 12 }}>
              Amount: {p.amount} ({p.method})
            </div>
            <div style={{ fontSize: 12 }}>
              Status: {p.status}
            </div>
          </div>

          {p.status === "pending" ? (
            <div style={{ display: "flex", gap: 8 }}>
              <ConfirmAction
                label="Approve"
                onConfirm={() => approve(p.id)}
              />
              <ConfirmAction
                label="Reject"
                danger
                onConfirm={() => reject(p.id)}
              />
            </div>
          ) : (
            <span style={{ fontSize: 12, color: "#999" }}>
              Processed
            </span>
          )}
        </div>
      ))}
    </div>
  );
}
