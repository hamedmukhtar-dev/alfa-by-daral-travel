type Props = {
  score: "high" | "medium" | "low";
};

export default function IntentBadge({ score }: Props) {
  const styles: Record<string, React.CSSProperties> = {
    high: {
      background: "#DCFCE7",
      color: "#166534",
      border: "1px solid #86EFAC",
    },
    medium: {
      background: "#FEF3C7",
      color: "#92400E",
      border: "1px solid #FDE68A",
    },
    low: {
      background: "#FEE2E2",
      color: "#991B1B",
      border: "1px solid #FCA5A5",
    },
  };

  const labels: Record<string, string> = {
    high: "🔴 جاد",
    medium: "🟡 متوسط",
    low: "⚪ استفسار",
  };

  return (
    <span
      style={{
        padding: "4px 8px",
        fontSize: 12,
        borderRadius: 6,
        fontWeight: 600,
        ...styles[score],
      }}
    >
      {labels[score]}
    </span>
  );
}
