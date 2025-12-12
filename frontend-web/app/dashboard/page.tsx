"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

type Request = {
  id: number;
  service_type: string;
  status: string;
  payment_method?: string;
  reference_note?: string;
};

export default function AdminRequests() {
  const [requests, setRequests] = useState<Request[]>([]);
  const [msg, setMsg] = useState("");

  const loadRequests = async () => {
    const res = await api.get("/admin/requests");
    setRequests(res.data);
  };

  const updateStatus = async (id: number, action: "approve" | "reject") => {
    await api.post(`/admin/requests/${id}/${action}`);
    setMsg(`Request ${id} ${action}d`);
    loadRequests();
  };

  useEffect(() => {
    loadRequests();
  }, []);

  return (
    <main>
      <h2>Admin — Service Requests</h2>

      {msg && <p>{msg}</p>}

      {requests.map((r) => (
        <div key={r.id} style={{ border: "1px solid #ccc", padding: 10, marginBottom: 10 }}>
          <p><b>ID:</b> {r.id}</p>
          <p><b>Service:</b> {r.service_type}</p>
          <p><b>Status:</b> {r.status}</p>

          <button onClick={() => updateStatus(r.id, "approve")}>
            Approve
          </button>
          <button onClick={() => updateStatus(r.id, "reject")} style={{ marginLeft: 10 }}>
            Reject
          </button>
        </div>
      ))}
    </main>
  );
}
