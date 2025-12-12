"use client";

import { useState } from "react";

export default function AIPage() {
  const [msg, setMsg] = useState("");

  return (
    <main style={{ padding: 40 }}>
      <h3>ALFA AI Assistant</h3>

      <input
        value={msg}
        onChange={(e) => setMsg(e.target.value)}
        placeholder="Ask ALFA..."
      />
      <button onClick={() => alert("AI Response (Demo)")}>Send</button>
    </main>
  );
}
