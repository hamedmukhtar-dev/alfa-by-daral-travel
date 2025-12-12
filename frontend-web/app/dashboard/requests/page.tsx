"use client";

export default function RequestsPage() {
  return (
    <main style={{ padding: 40 }}>
      <h3>Create Service Request</h3>

      <input placeholder="Service Type (Travel, Delivery, Telecom)" /><br /><br />
      <textarea placeholder="Details" /><br /><br />
      <button>Create Request</button>

      <p style={{ marginTop: 20 }}>✅ Request saved (Demo)</p>
    </main>
  );
}
