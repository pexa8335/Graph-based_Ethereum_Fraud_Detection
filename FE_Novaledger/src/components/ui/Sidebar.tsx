'use client';
import Image from 'next/image';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, Star, History, FileText, LogOut } from 'lucide-react';
const navItems = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'WatchList', href: '/watchlist', icon: Star },
    { name: 'History', href: '/history', icon: History },
    { name: 'Docs', href: '/docs', icon: FileText },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 flex-shrink-0 h-screen sticky top-0
                   bg-gradient-to-b from-slate-900 to-gray-900
                   border-r border-white/10 flex flex-col">
      <div className="flex items-center justify-center h-24 border-b border-white/10">
        <Image src="/logo.png" alt="NovaLedger Logo" width={40} height={40} />
        <span 
          className="ml-3 text-2xl font-bold text-white"
          style={{ textShadow: '0 1px 4px rgba(0,0,0,0.7)' }}
        >
          NovaLedger
        </span>
      </div>

      <nav className="flex-grow p-4">
        <ul>
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <li key={item.name}>
                <Link
                  href={item.href}
                  className={`flex items-center gap-4 px-4 py-3 my-2 rounded-lg text-sm font-medium transition-colors duration-200
                    ${
                      isActive
                        ? 'bg-cyan-400/20 text-white shadow-inner'
                        : 'text-gray-300 hover:bg-white/10 hover:text-white'
                    }`}
                >
                  <item.icon size={20} />
                  <span>{item.name}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
      <div className="p-4 border-t border-white/10">
        <Link
          href="/logout"
          className="flex items-center gap-4 px-4 py-3 rounded-lg text-gray-300 hover:bg-red-500/20 hover:text-white transition-colors duration-200"
        >
          <LogOut size={20} />
          <span className="text-sm font-medium">Log Out</span>
        </Link>
      </div>
    </aside>
  );
}