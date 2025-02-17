import type { Metadata } from 'next'
import { Geist, Geist_Mono } from "next/font/google";
import '@fortawesome/fontawesome-free/css/all.min.css';
import "./globals.css";
import { Header } from '@/components/Header/Header';

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: process.env.NAME || "NOOGA BITES",
  description: process.env.TAGLINE || "Discover Chattanooga's Best Eats – One Bite at a Time!",
  icons: {
    icon: '/icon.ico',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased overflow-x-hidden`}
      >
        <Header />
        <main className="min-h-screen bg-gray-50 py-6 overflow-x-hidden">
          {children}
        </main>
      </body>
    </html>
  )
}
