import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "MemVoice - Memory-Optimized Voice Agent",
  description:
    "Transform websites into interactive voice assistants with intelligent memory management",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
