"use client";

export default function PilotBanner() {
  const isPilot = process.env.NEXT_PUBLIC_APP_ENV === "pilot";
  if (!isPilot) return null;

  return (
    <div className="w-full px-4 py-2 text-sm border-b bg-yellow-50 text-yellow-900 flex flex-col md:flex-row md:items-center md:justify-between gap-1">
      <span>
        ⚠️ <strong>تشغيل تجريبي (Pilot Mode):</strong> المنصة قيد التطوير،
        والخدمات والأسعار المعروضة تقديرية، والتنفيذ يتم عبر مزودي خدمات
        ووكلاء مستقلين.
      </span>
      <span className="font-semibold">
        © {new Date().getFullYear()} Dar Alkhartoum Travel & Tourism Co. Ltd
      </span>
    </div>
  );
}
