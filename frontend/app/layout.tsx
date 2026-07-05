import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Dharma Knowledge Graph",
  description: "Epistemic knowledge navigation for Buddhist concepts"
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
