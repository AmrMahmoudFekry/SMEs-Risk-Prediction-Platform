'use client';

import { Activity, Database, GitMerge, ShieldCheck } from 'lucide-react';

export default function AnalyticsCenter() {
  return (
    <div className="min-h-full px-8 py-8">
      <div className="mb-8">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Analytics Console</p>
            <h1 className="mt-3 text-4xl font-semibold text-white">Model Performance & Explainability</h1>
            <p className="mt-3 max-w-2xl text-slate-400">Inspect predictive power, feature importance, and AI quality metrics for risk decisions.</p>
          </div>
          <div className="rounded-3xl border border-slate-800 bg-slate-950/80 px-6 py-4 text-right">
            <p className="text-sm text-slate-400">Latest refresh</p>
            <p className="mt-2 text-lg font-semibold text-white">2 minutes ago</p>
          </div>
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <section className="space-y-6">
          <div className="grid gap-6 md:grid-cols-4">
            <MetricCard title="Test ROC AUC" value="97.95%" icon={Activity} />
            <MetricCard title="F1 Score" value="91.25%" icon={GitMerge} />
            <MetricCard title="Precision" value="93.19%" icon={ShieldCheck} />
            <MetricCard title="Accuracy" value="91.94%" icon={Database} />
          </div>

          <div className="rounded-3xl border border-slate-800 bg-slate-950/80 p-6 shadow-[0_25px_60px_rgba(15,23,42,0.35)]">
            <h2 className="text-xl font-semibold text-white mb-4">Financial Relationship Analysis</h2>
            <p className="text-slate-400 mb-6">Compare debt-to-income metrics with cash flow signals to identify where risk concentration is highest.</p>
            <div className="grid gap-4 lg:grid-cols-2">
              <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-5">
                <div className="h-52 rounded-3xl bg-slate-800/80 flex items-center justify-center text-slate-500">[Scatter chart]</div>
              </div>
              <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-5">
                <div className="h-52 rounded-3xl bg-slate-800/80 flex items-center justify-center text-slate-500">[Bar chart]</div>
              </div>
            </div>
          </div>
        </section>

        <aside className="space-y-6">
          <div className="rounded-3xl border border-slate-800 bg-slate-950/80 p-6 shadow-[0_25px_60px_rgba(15,23,42,0.35)]">
            <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Dataset Summary</p>
            <div className="mt-6 grid gap-4">
              <SummaryCard label="Total records" value="35,000" />
              <SummaryCard label="Features" value="10" />
              <SummaryCard label="Low risk" value="18,550" />
              <SummaryCard label="High risk" value="16,450" />
            </div>
          </div>

          <div className="rounded-3xl border border-slate-800 bg-slate-950/80 p-6 shadow-[0_25px_60px_rgba(15,23,42,0.35)]">
            <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Operational insight</p>
            <p className="mt-4 text-slate-300 leading-7">Feature transparency helps risk teams understand why the model flags a business as high risk and speeds up review cycles.</p>
          </div>
        </aside>
      </div>
    </div>
  );
}

function MetricCard({ title, value, icon: Icon }: { title: string; value: string; icon: any }) {
  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-950/80 p-6 shadow-[0_20px_40px_rgba(15,23,42,0.35)]">
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm font-medium text-slate-400">{title}</p>
        <Icon className="h-5 w-5 text-slate-400" />
      </div>
      <p className="text-3xl font-semibold text-white">{value}</p>
    </div>
  );
}

function SummaryCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-5">
      <p className="text-sm text-slate-400">{label}</p>
      <p className="mt-3 text-2xl font-semibold text-white">{value}</p>
    </div>
  );
}
