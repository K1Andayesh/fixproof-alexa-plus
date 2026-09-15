import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "FixProof MCP · Live judge endpoint",
  description: "A public Streamable HTTP MCP endpoint for fictional, source-backed FixProof evaluations.",
  other: {
    "codex-preview": "development",
  },
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
