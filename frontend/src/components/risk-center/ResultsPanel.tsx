'use client';

import { useAssessmentStore } from '@/store/useAssessmentStore';
import { AlertOctagon, CheckCircle2, ShieldAlert, Download, RefreshCcw } from 'lucide-react';

export default function ResultsPanel() {
  const { smeData, resetForm } = useAssessmentStore();
  const result = smeData.assessmentResult;

  if (!result) return null;

  const isHighRisk = result.risk_profile.risk_score >= 70;
  const isMediumRisk = result.risk_profile.risk_score >= 40 && result.risk_profile.risk_score < 70;

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
        <button className="px-5 py-2.5 flex items-center gap-2 bg-slate-900 text-white dark:bg-slate-100 dark:text-slate-900 rounded-md hover:opacity-90 transition-opacity">
          <Download size={16} /> Export Enterprise PDF
        </button>
      </div>
    </div>
  );
}