'use client';

import { useState } from 'react';
import { useAssessmentStore } from '@/store/useAssessmentStore';
import { apiClient } from '@/lib/api-client';
import { Loader2 } from 'lucide-react';

export default function FinancialInfoStep() {
  const { smeData, updateSmeData, setStep, setProcessing, isProcessing } = useAssessmentStore();
  const [error, setError] = useState('');

  const handlePredict = async () => {
    setProcessing(true);
    setError('');

    if (!smeData.sme_id) {
      setError('SME ID is required to run the assessment.');
      setProcessing(false);
      return;
    }

    try {
      const response = await apiClient.post('/assessment/single', {
        sme_id: smeData.sme_id,
        financials: {
          legal_name: smeData.legal_name,
          industry: smeData.industry,
          business_age_months: smeData.business_age_months || 24,
          owner_credit_score: smeData.owner_credit_score || 650,
          credit_amount: smeData.credit_amount || 0,
          monthly_income_avg: smeData.monthly_income_avg || 0,
          total_deposits_3m: smeData.total_deposits_3m || 0,
          nsf_count_3m: smeData.nsf_count_3m || 0,
        },
      });

      updateSmeData({ assessmentResult: response.data });
      setStep(3);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred during assessment.');
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="p-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <h2 className="text-xl font-semibold mb-6">Financial & Banking Metrics</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Requested Credit Amount (EGP)</label>
          <input 
            type="number" 
            className="w-full bg-slate-50 dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-md px-4 py-2.5 focus:ring-2 focus:ring-blue-600 outline-none"
            onChange={(e) => updateSmeData({ credit_amount: Number(e.target.value) })}
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Average Monthly Income</label>
          <input 
            type="number" 
            className="w-full bg-slate-50 dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-md px-4 py-2.5 focus:ring-2 focus:ring-blue-600 outline-none"
            onChange={(e) => updateSmeData({ monthly_income_avg: Number(e.target.value) })}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Total Deposits (3 Months)</label>
          <input 
            type="number" 
            className="w-full bg-slate-50 dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-md px-4 py-2.5 focus:ring-2 focus:ring-blue-600 outline-none"
            onChange={(e) => updateSmeData({ total_deposits_3m: Number(e.target.value) })}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">NSF Count (Bounced Checks)</label>
          <input 
            type="number" 
            className="w-full bg-slate-50 dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-md px-4 py-2.5 focus:ring-2 focus:ring-blue-600 outline-none"
            onChange={(e) => updateSmeData({ nsf_count_3m: Number(e.target.value) })}
          />
        </div>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 text-red-600 dark:bg-red-900/20 dark:text-red-400 rounded-md border border-red-200 dark:border-red-800">
          {error}
        </div>
      )}

      <div className="flex justify-between mt-10">
        <button 
          onClick={() => setStep(1)}
          className="px-6 py-2.5 text-slate-600 border border-slate-300 rounded-md hover:bg-slate-50 transition-colors"
        >
          Back
        </button>
        <button 
          onClick={handlePredict}
          disabled={isProcessing}
          className="px-6 py-2.5 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors flex items-center gap-2 disabled:opacity-70"
        >
          {isProcessing && <Loader2 className="animate-spin w-4 h-4" />}
          {isProcessing ? 'Analyzing Risk...' : 'Run AI Assessment'}
        </button>
      </div>
    </div>
  );
}