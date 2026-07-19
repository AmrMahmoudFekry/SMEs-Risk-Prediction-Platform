'use client';

// src/app/(dashboard)/layout.tsx
import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';
import { 
  LayoutDashboard, 
  ActivitySquare, 
  BarChart3, 
  FileText, 
  Settings 
} from 'lucide-react';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, isLoading, logout } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-950 text-white">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
      </div>
    );
  }

  if (!user) {
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
    return null;
  }
  return (
    <div className="flex h-screen bg-slate-50 dark:bg-[#0F172A] overflow-hidden">
      {/* Enterprise Sidebar */}
      <aside className="w-64 bg-white dark:bg-[#1E293B] border-r border-slate-200 dark:border-slate-800 flex flex-col transition-colors duration-300">
        <div className="h-16 flex items-center px-6 border-b border-slate-200 dark:border-slate-800">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-md flex items-center justify-center">
              <ActivitySquare className="text-white w-5 h-5" />
            </div>
            <span className="font-bold text-lg text-slate-900 dark:text-white tracking-tight">
              SME Risk <span className="text-blue-600 dark:text-blue-500">Engine</span>
            </span>
          </div>
        </div>

        <nav className="flex-1 overflow-y-auto py-6 px-4 space-y-1">
          <NavItem href="/executive" icon={<LayoutDashboard size={20} />} label="Executive Dashboard" />
          <NavItem href="/risk-center" icon={<ActivitySquare size={20} />} label="Risk Assessment" />
          <NavItem href="/analytics" icon={<BarChart3 size={20} />} label="Model Analytics" />
          <NavItem href="/reports" icon={<FileText size={20} />} label="Enterprise Reports" />
        </nav>

        {user.role === 'Admin' && (
          <div className="p-4 border-t border-slate-200 dark:border-slate-800">
            <NavItem href="/settings" icon={<Settings size={20} />} label="System Settings" />
          </div>
        )}
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Top Header (User Profile, Notifications, etc.) */}
        <header className="h-16 bg-white/50 dark:bg-[#1E293B]/50 backdrop-blur-sm border-b border-slate-200 dark:border-slate-800 flex items-center justify-between px-8">
           <h2 className="text-sm font-medium text-slate-500 dark:text-slate-400">
             Financial Institution Portal
           </h2>
           <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm font-medium text-slate-900 dark:text-slate-100">{user.name}</p>
                <p className="text-xs text-slate-500 dark:text-slate-400">{user.role} • Org {user.organization_id}</p>
              </div>
              <button
                type="button"
                onClick={logout}
                className="rounded-full bg-slate-100 dark:bg-slate-700 px-3 py-1 text-xs font-semibold text-slate-900 dark:text-slate-100 hover:bg-slate-200 dark:hover:bg-slate-600 transition"
              >
                Sign out
              </button>
           </div>
        </header>

        {/* Page Content */}
        <div className="flex-1 overflow-auto">
          {children}
        </div>
      </main>
    </div>
  );
}

// مكون مساعد لعناصر القائمة الجانبية
function NavItem({ href, icon, label }: { href: string, icon: React.ReactNode, label: string }) {
  return (
    <Link 
      href={href}
      className="flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white transition-all"
    >
      {icon}
      {label}
    </Link>
  );
}