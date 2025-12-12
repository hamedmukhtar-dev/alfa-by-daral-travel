"use client";

import { useEffect, useState } from "react";
import { api } from "@/app/lib/api";
import ConfirmAction from "@/app/components/ConfirmAction";

type Wallet = {
  user_id: number;
  balance: number;
  pending_amount: number;
};

export default function WalletAdminPage() {
  const [wallets, setWallets] = useState<Wallet[]>([]);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const res = await api.get("/admin/reports/wallets");
      setWallets(res.data);
    } catch {
      alert("Failed to load wallets");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const approvePending = async (user_id: number, amount: number) => {
    await api.post("/wallet/admin/approve-offline-credit", {
      user_id,
      amount,
    });
    await load();
  };

  if (loading) return <div style={{ padding: 20 }}>Loading…</div>;

  return (
    <div style={{ padding: 20 }}>
      <h2 style={{ marginBottom: 12 }}>Wallets (Admin)</h2>

      {wallets.length === 0 && <p>No wallets</p>}

      {wallets.map((w) => (
        <div
          key={w.user_id}
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
            <strong>User #{w.user_id}</strong>
            <div style={{ fontSize: 12 }}>Balance: {w.balance}</div>
            <div style={{ fontSize: 12 }}>
              Pending: {w.pending_amount}
            </div>
          </div>

          {w.pending_amount > 0 ? (
            <ConfirmAction
              label="Approve Pending"
              onConfirm={() =>
                approvePending(w.user_id, w.pending_amount)
              }
            />
          ) : (
            <span style={{ fontSize: 12, color: "#999" }}>
              No pending
            </span>
          )}
        </div>
      ))}
    </div>
  );
}
