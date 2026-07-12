'use client';

import { useAssessmentStore } from '@/store/useAssessmentStore';
import { Building2, Landmark, CheckCircle } from 'lucide-react';
import BusinessInfoStep from '@/components/risk-center/BusinessInfoStep';
import FinancialInfoStep from '@/components/risk-center/FinancialInfoStep';
import ResultsPanel from '@/components/risk-center/ResultsPanel';

export default function RiskCenterPage() {
  const { step } = useAssessmentStore();

  const steps = [
    { num: 1, title: 'Business Profile', icon: Building2 },
    { num: 2, title: 'Financial Metrics', icon: Landmark },
    { num: 3, title: 'Assessment Results', icon: CheckCircle },
  ];

  return (
    <div className="min-h-full px-8 py-8">
      <div className="mb-8">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Risk Prediction Workflow</p>
            <h1 className="mt-3 text-4xl font-semibold text-white">SME Credit Assessment</h1>
          </div>
          <div className="rounded-3xl border border-slate-800 bg-slate-950/80 px-6 py-4 text-right">
            <p className="text-sm text-slate-400">Step progress</p>
            <p className="mt-2 text-lg font-semibold text-white">{step} of 3</p>
          </div>
        </div>
        <p className="mt-4 max-w-2xl text-slate-400">Complete the most relevant business and financial inputs to generate an intelligent risk score.</p>
      </div>

      <div className="mb-10 rounded-3xl border border-slate-800 bg-slate-950/80 p-5 shadow-[0_25px_60px_rgba(15,23,42,0.35)]">
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {steps.map((s) => (
            <div key={s.num} className={`rounded-3xl border p-4 ${step >= s.num ? 'border-blue-500/30 bg-slate-900/80' : 'border-slate-800 bg-slate-950/80'}`}>
              <div className="flex items-center gap-3">
                <div className="grid h-11 w-11 place-items-center rounded-2xl bg-blue-500/10 text-blue-400">{s.num}</div>
                <div>
                  <p className="text-xs uppercase tracking-[0.2em] text-slate-500">Step {s.num}</p>
                  <p className="mt-2 text-sm font-semibold text-white">{s.title}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="rounded-3xl border border-slate-800 bg-slate-950/90 shadow-[0_25px_60px_rgba(15,23,42,0.35)]">
        {step === 1 && <BusinessInfoStep />}
        {step === 2 && <FinancialInfoStep />}
        {step === 3 && <ResultsPanel />}
      </div>
    </div>
  );
}
