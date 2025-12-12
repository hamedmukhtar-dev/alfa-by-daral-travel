export default function Footer() {
  return (
    <footer
      style={{
        padding: 16,
        fontSize: 12,
        color: "#666",
        borderTop: "1px solid #eee",
        marginTop: 40,
      }}
    >
      <p>
        © {new Date().getFullYear()} Dar Alkhartoum Travel & Tourism Co. Ltd — ALFA
        operates in Pilot Mode. Execution via independent providers.
      </p>

      <p style={{ marginTop: 8 }}>
        <a href="/services">الخدمات</a> ·{" "}
        <a href="/requests/new">اطلب خدمة</a> ·{" "}
        <a href="/agent/onboarding">دليل الوكلاء</a> ·{" "}
        <a href="/supplier/onboarding">دليل مزودي الخدمات</a>
      </p>

      <p style={{ marginTop: 6 }}>
        <a href="/compliance">الامتثال والسياسات</a> ·{" "}
        <a href="/ai-policy">سياسة الذكاء الاصطناعي</a>
      </p>
    </footer>
  );
}
