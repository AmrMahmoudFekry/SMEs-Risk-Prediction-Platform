'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api-client';
import { Briefcase, AlertOctagon, CheckCircle, Target } from 'lucide-react';
import RiskTrendChart from '@/components/charts/RiskTrendChart';

const initialStats = {
  total_smes: 0,
  high_risk_count: 0,
  medium_risk_count: 0,
  low_risk_count: 0,
  average_confidence: 0,
};

export default function ExecutiveDashboard() {
  const [stats, setStats] = useState(initialStats);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await apiClient.get('/analytics/dashboard-stats');
        if (response?.data) setStats(response.data);
      } catch (error) {
        console.error('Error fetching stats:', error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (isLoading) {
    return (
      <div className="flex h-full items-center justify-center p-8">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
      </div>
    );
  }

  return (
    <div className="min-h-full px-8 py-8">
      <div className="mb-8">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Executive Overview</p>
            <h1 className="mt-3 text-4xl font-semibold text-white">SME Risk Portfolio Insight</h1>
            <p className="mt-3 max-w-2xl text-slate-400">Monitor portfolio health and risk exposure with AI-powered enterprise analytics.</p>
          </div>
          <div className="rounded-3xl border border-slate-800 bg-slate-950/80 px-6 py-4 text-right">
            <p className="text-sm text-slate-400">Current status</p>
            <p className="mt-2 text-lg font-semibold text-white">Operational</p>
          </div>
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.4fr_0.85fr]">
        <section className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
            <DashCard title="Total assessments" value={stats.total_smes} icon={Briefcase} accent="from-sky-500 to-blue-500" />
            <DashCard title="High risk cases" value={stats.high_risk_count} icon={AlertOctagon} accent="from-red-500 to-orange-500" />
            <DashCard title="Low risk cases" value={stats.low_risk_count} icon={CheckCircle} accent="from-emerald-500 to-teal-500" />
            <DashCard title="Avg confidence" value={`${stats.average_confidence}%`} icon={Target} accent="from-violet-500 to-fuchsia-500" />
          </div>

          <div className="rounded-3xl border border-slate-800 bg-slate-950/90 p-6 shadow-[0_25px_60px_rgba(15,23,42,0.35)]">
            <div className="flex items-center justify-between gap-4 mb-6">
              <div>
                <p className="text-sm text-slate-400">Risk evolution</p>
                <h2 className="text-2xl font-semibold text-white">Portfolio Risk Movement</h2>
              </div>
            </div>
            <div className="h-[360px]">
              <RiskTrendChart />
            </div>
          </div>
        </section>

        <aside className="space-y-6">
          <div className="rounded-3xl border border-slate-800 bg-slate-950/90 p-6 shadow-[0_25px_60px_rgba(15,23,42,0.35)]">
            <p className="text-sm uppercase tracking-[0.24em] text-slate-400">System readiness</p>
            <div className="mt-6 grid gap-4">
              <StatusChip label="Dataset" value="Ready" />
              <StatusChip label="Pipeline" value="Ready" />
              <StatusChip label="Model summary" value="Ready" />
            </div>
          </div>

          <div className="rounded-3xl border border-slate-800 bg-slate-950/90 p-6 shadow-[0_25px_60px_rgba(15,23,42,0.35)]">
            <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Strategic insight</p>
            <p className="mt-4 text-slate-300 leading-7">This executive console surfaces the most material risk patterns across the SME portfolio to support quick strategic decisions.</p>
          </div>
        </aside>
      </div>
    </div>
  );
}

function DashCard({ title, value, icon: Icon, accent }: { title: string; value: string | number; icon: any; accent: string }) {
  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-950/90 p-6 shadow-[0_25px_40px_rgba(15,23,42,0.35)]">
      <div className="flex items-center justify-between gap-4">
        <p className="text-sm text-slate-400">{title}</p>
        <div className="grid h-11 w-11 place-items-center rounded-2xl bg-slate-900/90 text-slate-300">
          <Icon className="h-5 w-5" />
        </div>
      </div>
      <p className="mt-4 text-3xl font-semibold text-white">{value}</p>
      <div className={`mt-6 h-1 rounded-full bg-gradient-to-r ${accent}`} />
    </div>
  );
}

function StatusChip({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between rounded-2xl bg-slate-900/80 px-4 py-3 border border-slate-800">
      <span className="text-sm text-slate-300">{label}</span>
      <span className="rounded-full bg-slate-800 px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] text-emerald-300">{value}</span>
    </div>
  );
}
