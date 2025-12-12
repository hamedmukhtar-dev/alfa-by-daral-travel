"use client";

import { useRouter } from "next/navigation";

export default function Dashboard() {
  const router = useRouter();

  return (
    <main style={{ padding: 40 }}>
      <h2>ALFA Dashboard</h2>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 20 }}>
        <button onClick={() => router.push("/dashboard/requests")}>
          📄 Service Requests
        </button>

        <button onClick={() => router.push("/dashboard/wallet")}>
          💳 Wallet (Demo)
        </button>

        <button onClick={() => router.push("/dashboard/ai")}>
          🤖 AI Assistant
        </button>

        <button onClick={() => alert("Travel Module (Demo)")}>
          ✈️ Travel
        </button>
      </div>
    </main>
  );
}
