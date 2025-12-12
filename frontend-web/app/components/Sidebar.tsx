"use client";

import Link from "next/link";

type Props = {
  role?: "admin" | "agent" | "supplier" | "user";
};

export default function Sidebar({ role }: Props) {
  return (
    <aside
      style={{
        width: 240,
        padding: 16,
        borderRight: "1px solid #eee",
        minHeight: "100vh",
      }}
    >
      <h3 style={{ marginBottom: 16 }}>ALFA Console</h3>

      {/* ---------------- Admin ---------------- */}
      {role === "admin" && (
        <ul style={{ listStyle: "none", padding: 0 }}>
          <li>
            <Link href="/dashboard">📊 لوحة التحكم</Link>
          </li>
          <li>
            <Link href="/requests">🧾 كل الطلبات</Link>
          </li>
          <li>
            <Link href="/reports">📈 التقارير</Link>
          </li>
          <li>
            <Link href="/dashboard/feedback">🗣️ تحليلات الآراء</Link>
          </li>
          <li>
            <Link href="/dashboard/alerts">🚨 التنبيهات</Link>
          </li>
          <li>
            <Link href="/audit">🛡️ سجل التدقيق</Link>
          </li>
        </ul>
      )}

      {/* ---------------- Agent ---------------- */}
      {role === "agent" && (
        <ul style={{ listStyle: "none", padding: 0 }}>
          <li>
            <Link href="/agent/requests">🧾 طلبات الوكيل</Link>
          </li>
          <li>
            <Link href="/agent/onboarding">📘 دليل الوكلاء</Link>
          </li>
        </ul>
      )}

      {/* ---------------- Supplier ---------------- */}
      {role === "supplier" && (
        <ul style={{ listStyle: "none", padding: 0 }}>
          <li>
            <Link href="/supplier/listings">🧩 خدماتي</Link>
          </li>
          <li>
            <Link href="/supplier/onboarding">📘 دليل مزودي الخدمات</Link>
          </li>
        </ul>
      )}

      {/* ---------------- Public / User ---------------- */}
      {!role && (
        <ul style={{ listStyle: "none", padding: 0 }}>
          <li>
            <Link href="/services">🌍 الخدمات</Link>
          </li>
          <li>
            <Link href="/requests/new">✍️ اطلب خدمة</Link>
          </li>
          <li>
            <Link href="/feedback">💬 رأيك يهمنا</Link>
          </li>
        </ul>
      )}
    </aside>
  );
}
