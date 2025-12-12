import PilotBanner from "@/app/components/PilotBanner";
import Footer from "@/app/components/Footer";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ar">
      <body style={{ margin: 0, fontFamily: "sans-serif" }}>
        <PilotBanner />
        {children}
        <Footer />
      </body>
    </html>
  );
}
