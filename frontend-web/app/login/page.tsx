"use client";

import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();

  const handleLogin = () => {
    // Demo login (no backend yet)
    localStorage.setItem("demo_token", "ALFA_DEMO_TOKEN");
    router.push("/dashboard");
  };

  return (
    <main style={{ padding: 40, maxWidth: 400 }}>
      <h2>ALFA Login (Demo)</h2>
      <input placeholder="Email" style={{ width: "100%" }} /><br /><br />
      <input placeholder="Password" type="password" style={{ width: "100%" }} /><br /><br />
      <button onClick={handleLogin}>Login</button>
    </main>
  );
}
