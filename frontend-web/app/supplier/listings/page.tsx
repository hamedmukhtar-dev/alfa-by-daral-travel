"use client";

import { useEffect, useState } from "react";
import { api } from "@/app/lib/api";

export default function SupplierListingsPage() {
  const [items, setItems] = useState<any[]>([]);

  useEffect(() => {
    api.get("/supplier/listings").then((res) => setItems(res.data));
  }, []);

  return (
    <main style={{ padding: 20 }}>
      <h1>خدماتي</h1>

      {items.length === 0 && <p>لا توجد خدمات مضافة</p>}

      {items.map((i) => (
        <div key={i.id} style={{ border: "1px solid #ddd", padding: 12, marginBottom: 8 }}>
          <strong>{i.title}</strong>
          <div>{i.category}</div>
          <div>{i.city} {i.country}</div>
          <div>
            السعر: {i.price_from} - {i.price_to} {i.currency}
          </div>
        </div>
      ))}
    </main>
  );
}
