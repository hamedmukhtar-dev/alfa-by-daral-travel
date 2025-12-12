"use client";

import { useEffect, useState } from "react";
import { api } from "@/app/lib/api";

type AuditLog = {
  id: number;
  admin_id: number;
  action: string;
  target_type: string;
  target_id: number | null;
  description: string | null;
  created_at: string;
};

export default function AuditPage() {
  const [rows, setRows] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const res = await api.get("/admin/reports/audit");
      setRows(res.data);
    } catch {
      alert("Failed to load audit log");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  if (loading) return <div style={{ padding: 20 }}>Loading…</div>;

  return (
    <div style={{ padding: 20 }}>
      <h2 style={{ marginBottom: 12 }}>Admin Audit Log</h2>

      <button onClick={load} style={{ marginBottom: 10 }}>
        Refresh
      </button>

      {rows.length === 0 && <p>No audit entries</p>}

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          fontSize: 13,
        }}
      >
        <thead>
          <tr>
            <th>ID</th>
            <th>Admin</th>
            <th>Action</th>
            <th>Target</th>
            <th>Description</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.id}>
              <td>{r.id}</td>
              <td>{r.admin_id}</td>
              <td>{r.action}</td>
              <td>
                {r.target_type}
                {r.target_id ? ` #${r.target_id}` : ""}
              </td>
              <td>{r.description || "-"}</td>
              <td>{new Date(r.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
