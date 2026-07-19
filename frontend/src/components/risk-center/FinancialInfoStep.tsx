'use client';

import { useState } from 'react';
import { useAssessmentStore } from '@/store/useAssessmentStore';
import { apiClient } from '@/lib/api-client';
import { getErrorMessage } from '@/lib/get-error-message';
import { Loader2 } from 'lucide-react';

const REQUIRED_FIELDS: [string, string][] = [
  ['credit_amount', 'Requested credit amount'],
  ['monthly_income_avg', 'Average monthly income'],
  ['total_deposits_3m', 'Total deposits (3 months)'],
  ['nsf_count_3m', 'NSF count'],
  ['negative_days_3m', 'Negative balance days'],
  ['dti_monthly', 'Debt-to-income ratio'],
  ['revenue_volatility_3m', 'Revenue volatility'],
  ['request_ratio', 'Credit request ratio'],
  ['owner_percentage', 'Owner ownership percentage'],
  ['owner_credit_score', 'Owner credit score'],
  ['business_age_months', 'Business age'],
];

export default function FinancialInfoStep() {
  const { smeData, updateSmeData, setStep, setProcessing, isProcessing } = useAssessmentStore();
  const [error, setError] = useState('');

  const handlePredict = async () => {
    setProcessing(true);
    setError('');

    if (!smeData.sme_id) {
      setError('Please go back and select or create an SME first.');
      setProcessing(false);
      return;
    }

    const missing = REQUIRED_FIELDS.filter(
      ([key]) => smeData[key] === undefined || smeData[key] === '' || Number.isNaN(smeData[key])
    );
    if (missing.length > 0) {
      setError(`Please fill in: ${missing.map(([, label]) => label).join(', ')}.`);
      setProcessing(false);
      return;
    }

    try {
      const response = await apiClient.post('/assessment/single', {
        sme_id: smeData.sme_id,
        lang: 'en',
        financials: {
          credit_amount: smeData.credit_amount,
          monthly_income_avg: smeData.monthly_income_avg,
          total_deposits_3m: smeData.total_deposits_3m,
          nsf_count_3m: smeData.nsf_count_3m,
          negative_days_3m: smeData.negative_days_3m,
          dti_monthly: smeData.dti_monthly,
          revenue_volatility_3m: smeData.revenue_volatility_3m,
          request_ratio: smeData.request_ratio,
          owner_percentage: smeData.owner_percentage,
          owner_credit_score: smeData.owner_credit_score,
          business_age_months: smeData.business_age_months,
        },
      });

      updateSmeData({ assessmentResult: response.data });
      setStep(3);
    } catch (err: any) {
      setError(getErrorMessage(err, 'An error occurred during assessment.'));
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="p-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <h2 className="text-xl font-semibold mb-6">Financial & Banking Metrics</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <Field label="Requested Credit Amount (EGP)">
          <input
            type="number"
            className={inputClass}
            value={smeData.credit_amount ?? ''}
            onChange={(e) => updateSmeData({ credit_amount: Number(e.target.value) })}
          />
        </Field>

        <Field label="Average Monthly Income (EGP)">
          <input
            type="number"
            className={inputClass}
            value={smeData.monthly_income_avg ?? ''}
            onChange={(e) => updateSmeData({ monthly_income_avg: Number(e.target.value) })}
          />
        </Field>

        <Field label="Total Deposits, Last 3 Months (EGP)">
          <input
            type="number"
            className={inputClass}
            value={smeData.total_deposits_3m ?? ''}
            onChange={(e) => updateSmeData({ total_deposits_3m: Number(e.target.value) })}
          />
        </Field>

        <Field label="NSF Count (Bounced Checks, 3 Months)">
          <input
            type="number"
            min={0}
            className={inputClass}
            value={smeData.nsf_count_3m ?? ''}
            onChange={(e) => updateSmeData({ nsf_count_3m: Number(e.target.value) })}
          />
        </Field>

        <Field label="Negative Balance Days (out of last 90)" hint="Days the account balance was below zero">
          <input
            type="number"
            min={0}
            max={90}
            className={inputClass}
            value={smeData.negative_days_3m ?? ''}
            onChange={(e) => updateSmeData({ negative_days_3m: Number(e.target.value) })}
          />
        </Field>

        <Field label="Debt-to-Income Ratio (0 – 1)" hint="0 = no debt burden, 1 = fully leveraged">
          <input
            type="number"
            step={0.01}
            min={0}
            max={1}
            className={inputClass}
            value={smeData.dti_monthly ?? ''}
            onChange={(e) => updateSmeData({ dti_monthly: Number(e.target.value) })}
          />
        </Field>

        <Field label="Revenue Volatility (0 – 1)" hint="0 = perfectly stable revenue, 1 = highly volatile">
          <input
            type="number"
            step={0.01}
            min={0}
            max={1}
            className={inputClass}
            value={smeData.revenue_volatility_3m ?? ''}
            onChange={(e) => updateSmeData({ revenue_volatility_3m: Number(e.target.value) })}
          />
        </Field>

        <Field label="Credit Request Ratio" hint="Requested amount vs. this SME's typical financing need (1.0 = typical)">
          <input
            type="number"
            step={0.1}
            min={0}
            className={inputClass}
            value={smeData.request_ratio ?? ''}
            onChange={(e) => updateSmeData({ request_ratio: Number(e.target.value) })}
          />
        </Field>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 text-red-600 dark:bg-red-900/20 dark:text-red-400 rounded-md border border-red-200 dark:border-red-800 text-sm">
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

const inputClass =
  'w-full bg-slate-50 dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-md px-4 py-2.5 focus:ring-2 focus:ring-blue-600 outline-none transition-all';

function Field({ label, hint, children }: { label: string; hint?: string; children: React.ReactNode }) {
  return (
    <div>
      <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">{label}</label>
      {children}
      {hint && <p className="mt-1 text-xs text-slate-500 dark:text-slate-500">{hint}</p>}
    </div>
  );
}