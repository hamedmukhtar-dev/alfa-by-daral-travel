"use client";

import { useEffect, useState } from "react";
import { api } from "@/app/lib/api";

type CountItem = { [key: string]: any; count: number };

export default function FeedbackAnalyticsPage() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    api.get("/analytics/feedback").then((res) => setData(res.data));
  }, []);

  if (!data) return <p>جاري تحميل تحليلات الآراء...</p>;

  const Section = ({ title, items, keyName }: any) => (
    <>
      <h3>{title}</h3>
      <ul>
        {items.map((i: CountItem, idx: number) => (
          <li key={idx}>
            {i[keyName]}: {i.count}
          </li>
        ))}
      </ul>
    </>
  );

  return (
    <main style={{ padding: 24 }}>
      <h1>📊 تحليلات الآراء والمقترحات</h1>

      <Section
        title="حسب النوع"
        items={data.by_category}
        keyName="category"
      />

      <Section
        title="حسب المزاج"
        items={data.by_sentiment}
        keyName="sentiment"
      />

      <Section
        title="حسب الأولوية"
        items={data.by_priority}
        keyName="priority"
      />

      <h3>أحدث الآراء</h3>
      <ul>
        {data.latest.map((f: any) => (
          <li key={f.id} style={{ marginBottom: 8 }}>
            <strong>{f.ai_category}</strong> — {f.ai_sentiment} /{" "}
            {f.ai_priority}
            <br />
            {f.message}
          </li>
        ))}
      </ul>
    </main>
  );
}
