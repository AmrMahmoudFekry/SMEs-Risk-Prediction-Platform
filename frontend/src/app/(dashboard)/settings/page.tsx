'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { ShieldCheck, Users, Settings2 } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';

export default function SettingsPage() {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && user && user.role !== 'Admin') {
      router.replace('/executive');
    }
  }, [isLoading, user, router]);

  if (isLoading) {
    return (
      <div className="min-h-full px-8 py-8">
        <div className="flex h-64 items-center justify-center text-slate-300">Loading settings...</div>
      </div>
    );
  }

  if (!user || user.role !== 'Admin') {
    return (
      <div className="min-h-full px-8 py-8">
        <div className="rounded-3xl border border-slate-800 bg-slate-950/80 p-10 text-center text-slate-300">
          <p className="text-lg font-semibold text-white">Access denied</p>
          <p className="mt-3 text-slate-400">Only administrators can access the system settings console.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-full px-8 py-8">
      <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.24em] text-slate-400">System Settings</p>
          <h1 className="mt-3 text-4xl font-semibold text-white">Platform Configuration</h1>
          <p className="mt-3 max-w-2xl text-slate-400">Manage user roles, access controls and application settings from a secure admin console.</p>
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-[0.9fr_0.7fr]">
        <section className="rounded-3xl border border-slate-800 bg-slate-950/80 p-6 shadow-[0_25px_60px_rgba(15,23,42,0.35)]">
          <div className="mb-6">
            <h2 className="text-xl font-semibold text-white">Access Control</h2>
            <p className="mt-2 text-slate-400">Assign and update role permissions for platform users.</p>
          </div>
          <div className="grid gap-4">
            <SettingCard icon={Users} title="User management" description="Review registered users and roles." />
            <SettingCard icon={ShieldCheck} title="Role-based policies" description="Control access across dashboards and reports." />
            <SettingCard icon={Settings2} title="System preferences" description="Configure platform defaults and notifications." />
          </div>
        </section>

        <aside className="rounded-3xl border border-slate-800 bg-slate-950/80 p-6 shadow-[0_25px_60px_rgba(15,23,42,0.35)]">
          <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Admin summary</p>
          <div className="mt-6 space-y-4">
            <SummaryStat label="Active roles" value="3" />
            <SummaryStat label="Pending approvals" value="1" />
            <SummaryStat label="Security audits" value="Monthly" />
          </div>
          <button className="mt-8 w-full rounded-3xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white hover:bg-blue-500 transition">Review audit log</button>
        </aside>
      </div>
    </div>
  );
}

function SettingCard({ icon: Icon, title, description }: { icon: any; title: string; description: string }) {
  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-5 hover:border-blue-500 transition">
      <div className="flex items-center gap-3">
        <div className="grid h-12 w-12 place-items-center rounded-2xl bg-blue-500/10 text-blue-300">
          <Icon className="h-5 w-5" />
        </div>
        <div>
          <p className="text-sm font-semibold text-white">{title}</p>
          <p className="text-sm text-slate-400">{description}</p>
        </div>
      </div>
    </div>
  );
}

function SummaryStat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-4">
      <p className="text-sm text-slate-400">{label}</p>
      <p className="mt-2 text-2xl font-semibold text-white">{value}</p>
    </div>
  );
}
