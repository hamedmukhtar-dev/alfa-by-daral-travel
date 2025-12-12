"use client";

import { useEffect, useState } from "react";
import { api } from "@/app/lib/api";

export default function PublicServices() {
  const [services, setServices] = useState<any[]>([]);

  useEffect(() => {
    api.get("/public/services").then(res => setServices(res.data));
  }, []);

  return (
    <main style={{ padding: 32 }}>
      <h1>الخدمات المتاحة</h1>

      {services.length === 0 && <p>لا توجد خدمات حالياً</p>}

      {services.map(s => (
        <div key={s.id} style={{ border: "1px solid #ddd", padding: 12, marginBottom: 10 }}>
          <strong>{s.title}</strong>
          <div>{s.category}</div>
          <div>{s.city} {s.country}</div>
          <div>
            السعر التقريبي: {s.price_from} - {s.price_to} {s.currency}
          </div>
        </div>
      ))}
    </main>
  );
}
