"use client";

import Link from "next/link";

export default function PublicHome() {
  return (
    <main style={{ padding: 32 }}>
      <h1>ALFA by Daral Travel</h1>
      <p>
        منصة خدمات سفر وخدمات محلية — جمهور + وكلاء + مزودين
      </p>

      <div style={{ marginTop: 24 }}>
        <Link href="/services">
          <button>استعرض الخدمات</button>
        </Link>
        {" "}
        <Link href="/requests/new">
          <button>اطلب خدمة</button>
        </Link>
      </div>

      <p style={{ marginTop: 24, fontSize: 13, color: "#666" }}>
        ⚠️ المنصة تعمل في وضع Pilot — لا حجز مباشر ولا دفع إلكتروني
      </p>
    </main>
  );
}
