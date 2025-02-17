'use client';

import Image from 'next/image';
import Link from 'next/link';

export const Header = () => {
  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 flex items-center">
        <div className="logo">
          <Link href="/">
            <Image src="/images/NoogaBitesLogo.png" alt="Nooga Bites Logo" width={200} height={140} />
          </Link>
        </div>
        <div style={{ marginLeft: '50px' }}>
          <h1 className="text-2xl font-bold text-gray-900 mb-4">{process.env.NEXT_PUBLIC_NAME}</h1>
          <p className="text-sm text-gray-600">{process.env.NEXT_PUBLIC_TAGLINE}</p>
        </div>
      </div>
    </header>
  )
}
