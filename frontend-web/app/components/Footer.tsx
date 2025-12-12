export default function Footer() {
  return (
    <footer style={{ padding: 16, fontSize: 12, color: "#666", borderTop: "1px solid #eee" }}>
      <p>
        © {new Date().getFullYear()} Dar Alkhartoum Travel & Tourism Co. Ltd —
        ALFA operates in Pilot Mode. Execution via independent providers.
      </p>
      <p>
        <a href="/compliance">الامتثال والسياسات</a> ·{" "}
        <a href="/ai-policy">سياسة الذكاء الاصطناعي</a>
      </p>
    </footer>
  );
}
