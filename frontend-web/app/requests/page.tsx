"use client";

import { useState } from "react";
import { api } from "@/app/lib/api";

export default function NewRequestPage() {
  const [title, setTitle] = useState("");
  const [phone, setPhone] = useState("");

  const submit = async () => {
    await api.post("/requests", {
      category: "general",
      title,
      user_phone: phone
    });
    alert("تم إرسال الطلب بنجاح");
  };

  return (
    <main style={{ padding: 32 }}>
      <h1>طلب خدمة</h1>

      <input
        placeholder="وصف مختصر للخدمة"
        value={title}
        onChange={e => setTitle(e.target.value)}
      />
      <br /><br />
      <input
        placeholder="رقم الهاتف"
        value={phone}
        onChange={e => setPhone(e.target.value)}
      />
      <br /><br />
      <button onClick={submit}>إرسال الطلب</button>

      <p style={{ marginTop: 16, fontSize: 12, color: "#666" }}>
        ⚠️ لا يتم تنفيذ الطلب تلقائيًا — سيتم التواصل يدويًا
      </p>
    </main>
  );
}
