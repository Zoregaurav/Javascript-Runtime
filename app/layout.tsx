import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap"
});

export const metadata: Metadata = {
  title: "Agripick | Connecting Farms. Empowering Growth.",
  description:
    "Agripick helps farmers, buyers, and businesses build a smarter agricultural ecosystem through technology and transparency.",
  keywords: [
    "Agripick",
    "agritech",
    "farm to consumer",
    "farmer marketplace",
    "agriculture technology",
    "fresh produce logistics"
  ],
  openGraph: {
    title: "Agripick | Connecting Farms. Empowering Growth.",
    description:
      "A premium AgriTech platform connecting farmers, buyers, and food businesses through transparency, logistics, and data.",
    type: "website"
  }
};

export default function RootLayout({
  children
}: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} bg-cream text-slate-950 antialiased`}>
        {children}
      </body>
    </html>
  );
}
