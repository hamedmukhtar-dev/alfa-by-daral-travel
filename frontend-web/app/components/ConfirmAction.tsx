"use client";

import { useState } from "react";

export default function ConfirmAction({
  label,
  onConfirm,
  danger = false,
}: {
  label: string;
  onConfirm: () => Promise<void>;
  danger?: boolean;
}) {
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    const ok = window.confirm("هل أنت متأكد من تنفيذ هذا الإجراء؟");
    if (!ok) return;

    setLoading(true);
    try {
      await onConfirm();
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={handleClick}
      disabled={loading}
      style={{
        padding: "6px 10px",
        fontSize: "13px",
        borderRadius: 4,
        border: danger ? "1px solid #dc2626" : "1px solid #555",
        background: danger ? "#fee2e2" : "#f9fafb",
        color: danger ? "#991b1b" : "#111",
        opacity: loading ? 0.6 : 1,
        cursor: loading ? "not-allowed" : "pointer",
      }}
    >
      {loading ? "Processing..." : label}
    </button>
  );
}
