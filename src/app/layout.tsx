import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import "./globals.css";
import { Header } from '@/components/Header/Header';

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Chattanooga Restaurant Directory',
  description: 'Find and explore restaurants in Chattanooga',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link 
          href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"
          rel="stylesheet"
        />
      </head>
      <body className={`${inter.className} min-h-screen bg-gray-50 py-8 overflow-x-hidden font-sans antialiased`}>
        <Header />
        {children}
      </body>
    </html>
  )
}
