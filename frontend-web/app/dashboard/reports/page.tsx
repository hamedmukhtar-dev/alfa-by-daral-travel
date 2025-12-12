"use client";

import { useEffect, useState } from "react";
import { api } from "@/app/lib/api";

type KPIs = {
  users: { total: number; active: number };
  wallets: { total_balance: number; pending_credit: number };
  service_requests: { total: number; pending: number };
};

export default function ReportsPage() {
  const [data, setData] = useState<KPIs | null>(null);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const res = await api.get("/admin/reports/kpis");
      setData(res.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  if (loading) return <div className="p-6">Loading reports…</div>;
  if (!data) return <div className="p-6 text-red-600">No data</div>;

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Admin Reports (Live)</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <KpiBox title="Users" a={`Total: ${data.users.total}`} b={`Active: ${data.users.active}`} />
        <KpiBox title="Wallets" a={`Balance: ${data.wallets.total_balance}`} b={`Pending: ${data.wallets.pending_credit}`} />
        <KpiBox title="Requests" a={`Total: ${data.service_requests.total}`} b={`Pending: ${data.service_requests.pending}`} />
      </div>

      <button
        onClick={load}
        className="px-4 py-2 border rounded hover:bg-gray-100"
      >
        Refresh
      </button>
    </div>
  );
}

function KpiBox({ title, a, b }: { title: string; a: string; b: string }) {
  return (
    <div className="border rounded p-4">
      <h2 className="font-semibold mb-2">{title}</h2>
      <p>{a}</p>
      <p>{b}</p>
    </div>
  );
}
