'use client';

import { useAssessmentStore } from '@/store/useAssessmentStore';
import { AlertOctagon, CheckCircle2, ShieldAlert, Download, RefreshCcw, TrendingUp, TrendingDown } from 'lucide-react';

const PRIORITY_STYLES: Record<string, string> = {
  CRITICAL: 'bg-red-500/10 text-red-400 border-red-500/20',
  HIGH: 'bg-orange-500/10 text-orange-400 border-orange-500/20',
  MEDIUM: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
  LOW: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
};

export default function ResultsPanel() {
  const { smeData, resetForm } = useAssessmentStore();
  const result = smeData.assessmentResult;

  if (!result) return null;

  const isHighRisk = result.risk_profile.risk_score >= 70;
  const isMediumRisk = result.risk_profile.risk_score >= 40 && result.risk_profile.risk_score < 70;

  const topShap = (result.shap_contributions || []).slice(0, 5);
  const maxShapAbs = Math.max(...topShap.map((c: any) => Math.abs(c.shap_value)), 0.0001);

  return (
    <div className="p-8 animate-in fade-in zoom-in-95 duration-500">
      {/* Risk Score Header */}
      <div className={`p-6 rounded-xl border mb-8 flex items-center justify-between ${
        isHighRisk ? 'bg-red-50 border-red-200 dark:bg-red-900/10 dark:border-red-900' :
        isMediumRisk ? 'bg-amber-50 border-amber-200 dark:bg-amber-900/10 dark:border-amber-900' :
        'bg-green-50 border-green-200 dark:bg-green-900/10 dark:border-green-900'
      }`}>
        <div>
          <p className="text-sm font-semibold uppercase tracking-wider mb-1 opacity-80">
            Final Risk Score
          </p>
          <div className="flex items-end gap-4">
            <h2 className="text-5xl font-black">{result.risk_profile.risk_score}%</h2>
            <span className="text-lg font-medium mb-1">({result.risk_profile.risk_category})</span>
          </div>
          <p className="mt-2 text-sm opacity-80">
            AI Confidence Level: <strong>{result.risk_profile.confidence}%</strong>
          </p>
        </div>

        <div>
          {isHighRisk ? <AlertOctagon size={80} className="text-red-500 opacity-80" /> :
           isMediumRisk ? <ShieldAlert size={80} className="text-amber-500 opacity-80" /> :
           <CheckCircle2 size={80} className="text-green-500 opacity-80" />}
        </div>
      </div>

      {/* Top Risk Drivers (SHAP) */}
      {topShap.length > 0 && (
        <div className="mb-8">
          <h3 className="text-lg font-bold mb-4 border-b border-slate-200 dark:border-slate-700 pb-2">
            Top Risk Drivers
          </h3>
          <div className="space-y-3">
            {topShap.map((c: any) => {
              const widthPct = (Math.abs(c.shap_value) / maxShapAbs) * 100;
              const increasesRisk = c.direction === 'increases_risk';
              return (
                <div key={c.feature} className="flex items-center gap-3 text-sm">
                  <span className="w-40 shrink-0 text-slate-600 dark:text-slate-400 truncate">
                    {c.feature.replace(/_/g, ' ')}
                  </span>
                  <div className="flex-1 h-2 rounded-full bg-slate-100 dark:bg-slate-800 overflow-hidden">
                    <div
                      className={`h-full rounded-full ${increasesRisk ? 'bg-red-500' : 'bg-emerald-500'}`}
                      style={{ width: `${widthPct}%` }}
                    />
                  </div>
                  <span className={`flex items-center gap-1 w-28 shrink-0 justify-end text-xs font-medium ${increasesRisk ? 'text-red-500' : 'text-emerald-500'}`}>
                    {increasesRisk ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
                    {increasesRisk ? 'Increases risk' : 'Decreases risk'}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Deterministic Recommendations */}
      {result.recommendations?.length > 0 && (
        <div className="mb-8">
          <h3 className="text-lg font-bold mb-4 border-b border-slate-200 dark:border-slate-700 pb-2">
            Key Recommendations
          </h3>
          <div className="space-y-3">
            {result.recommendations.map((rec: any, i: number) => (
              <div key={i} className={`rounded-lg border p-4 ${PRIORITY_STYLES[rec.priority] || PRIORITY_STYLES.LOW}`}>
                <div className="flex items-center justify-between">
                  <p className="font-semibold text-slate-900 dark:text-white">{rec.title}</p>
                  <span className="text-xs font-bold uppercase tracking-wide">{rec.priority}</span>
                </div>
                <p className="mt-1 text-sm text-slate-700 dark:text-slate-300">{rec.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Gemini AI Recommendation */}
      <div className="mb-8">
        <h3 className="text-lg font-bold mb-4 border-b border-slate-200 dark:border-slate-700 pb-2">
          AI Credit Recommendation (Gemini)
        </h3>
        <div className="bg-slate-50 dark:bg-[#0F172A] p-6 rounded-lg border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 leading-relaxed whitespace-pre-wrap">
          {result.ai_insights}
        </div>
      </div>

      {/* Actions */}
      <div className="flex justify-end gap-4 pt-6 border-t border-slate-200 dark:border-slate-800">
        <button
          onClick={resetForm}
          className="px-5 py-2.5 flex items-center gap-2 text-slate-600 border border-slate-300 rounded-md hover:bg-slate-50 transition-colors"
        >
          <RefreshCcw size={16} /> New Assessment
        </button>
        <button
          disabled
          title="PDF export is not wired up yet"
          className="px-5 py-2.5 flex items-center gap-2 bg-slate-300 text-slate-500 dark:bg-slate-800 dark:text-slate-500 rounded-md cursor-not-allowed"
        >
          <Download size={16} /> Export Enterprise PDF (coming soon)
        </button>
      </div>
    </div>
  );
}