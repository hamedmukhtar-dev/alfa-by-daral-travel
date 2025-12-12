"use client";

import Link from "next/link";

export default function Sidebar() {
  return (
    <aside
      style={{
        width: 220,
        height: "100vh",
        background: "#0f172a",
        color: "#fff",
        padding: 20,
      }}
    >
      <h2 style={{ marginBottom: 30 }}>ALFA</h2>

      <nav style={{ display: "flex", flexDirection: "column", gap: 15 }}>
        <Link href="/dashboard">🏠 Dashboard</Link>
        <Link href="/dashboard/requests">📄 Requests</Link>
        <Link href="/dashboard/wallet">💳 Wallet</Link>
        <Link href="/dashboard/ai">🤖 AI</Link>
      </nav>
    </aside>
  );
}
