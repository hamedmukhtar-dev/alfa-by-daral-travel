"use client";

import { useEffect, useState } from "react";
import { api } from "@/app/lib/api";

type Report = {
  total_requests: number;
  high_intent_requests: number;
  high_intent_percentage: number;
  top_categories: { category: string; count: number }[];
  top_cities: { city: string; count: number }[];
};

export default function WeeklyReportPage() {
  const [data, setData] = useState<Report | null>(null);

  useEffect(() => {
    api.get("/reports/weekly").then((res) => setData(res.data));
  }, []);

  if (!data) return <p>جاري تحميل التقرير...</p>;

  return (
    <main style={{ padding: 20 }}>
      <h1>📊 التقرير الأسبوعي</h1>

      <p>إجمالي الطلبات: {data.total_requests}</p>
      <p>الطلبات الجادة: {data.high_intent_requests}</p>
      <p>
        نسبة الجدية: {data.high_intent_percentage}%
      </p>

      <h3>أكثر الفئات طلبًا</h3>
      <ul>
        {data.top_categories.map((c) => (
          <li key={c.category}>
            {c.category}: {c.count}
          </li>
        ))}
      </ul>

      <h3>أكثر المدن نشاطًا</h3>
      <ul>
        {data.top_cities.map((c) => (
          <li key={c.city}>
            {c.city}: {c.count}
          </li>
        ))}
      </ul>
    </main>
  );
}
