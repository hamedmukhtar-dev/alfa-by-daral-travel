"use client";

import { useEffect, useState } from "react";
import { api } from "@/app/lib/api";
import ConfirmAction from "@/app/components/ConfirmAction";

type Request = {
  id: number;
  service_type: string;
  status: string;
  user_id: number;
};

export default function RequestsPage() {
  const [data, setData] = useState<Request[]>([]);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const res = await api.get("/service-requests");
      setData(res.data);
    } catch (e) {
      alert("Failed to load requests");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const approve = async (id: number) => {
    await api.post("/admin/service-requests/approve", { request_id: id });
    await load();
  };

  const reject = async (id: number) => {
    await api.post("/admin/service-requests/reject", {
      request_id: id,
      reason: "Rejected by admin",
    });
    await load();
  };

  if (loading) return <div style={{ padding: 20 }}>Loading…</div>;

  return (
    <div style={{ padding: 20 }}>
      <h2 style={{ marginBottom: 12 }}>Service Requests (Pilot)</h2>

      {data.length === 0 && <p>No requests</p>}

      {data.map((r) => (
        <div
          key={r.id}
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
            <strong>#{r.id}</strong> — {r.service_type}  
            <div style={{ fontSize: 12, color: "#555" }}>
              Status: {r.status}
            </div>
          </div>

          {r.status === "pending" ? (
            <div style={{ display: "flex", gap: 8 }}>
              <ConfirmAction
                label="Approve"
                onConfirm={() => approve(r.id)}
              />
              <ConfirmAction
                label="Reject"
                danger
                onConfirm={() => reject(r.id)}
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
