"use client";

import { useEffect, useState } from "react";
import { api } from "@/app/lib/api";

type LedgerEntry = {
  id: number;
  user_id: number;
  wallet_id: number;
  type: string;
  amount: number;
  currency: string;
  reference: string | null;
  admin_id: number | null;
  created_at: string;
};

export default function LedgerPage() {
  const [rows, setRows] = useState<LedgerEntry[]>([]);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const res = await api.get("/admin/reports/ledger");
      setRows(res.data);
    } catch {
      alert("Failed to load ledger");
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
      <h2 style={{ marginBottom: 12 }}>Ledger (Read-Only)</h2>

      <button onClick={load} style={{ marginBottom: 10 }}>
        Refresh
      </button>

      {rows.length === 0 && <p>No ledger entries</p>}

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
            <th>User</th>
            <th>Type</th>
            <th>Amount</th>
            <th>Ref</th>
            <th>Admin</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.id}>
              <td>{r.id}</td>
              <td>{r.user_id}</td>
              <td>{r.type}</td>
              <td>
                {r.amount} {r.currency}
              </td>
              <td>{r.reference || "-"}</td>
              <td>{r.admin_id ?? "-"}</td>
              <td>{new Date(r.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
