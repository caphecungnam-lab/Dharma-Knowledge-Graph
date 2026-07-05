import type { Metadata } from "next";

import "../styles/globals.css";

export const metadata: Metadata = {
  title: "Dharma Knowledge Graph",
  description: "Epistemic knowledge graph navigation interface"
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
