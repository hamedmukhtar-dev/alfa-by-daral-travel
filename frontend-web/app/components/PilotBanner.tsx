"use client";

export default function PilotBanner() {
  const isPilot = process.env.NEXT_PUBLIC_APP_ENV === "pilot";
  if (!isPilot) return null;

  return (
    <div className="w-full px-4 py-2 text-sm border-b bg-yellow-50 text-yellow-900 flex items-center justify-between">
      <span>⚠️ Pilot Mode فعال — بعض الميزات تحت المراقبة</span>
      <span className="font-semibold">ALFA by Daral Travel</span>
    </div>
  );
}
