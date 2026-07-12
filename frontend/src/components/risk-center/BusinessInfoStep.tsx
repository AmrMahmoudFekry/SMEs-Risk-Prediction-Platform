'use client';

import { useAssessmentStore } from '@/store/useAssessmentStore';

export default function BusinessInfoStep() {
  const { smeData, updateSmeData, setStep } = useAssessmentStore();

  const handleNext = () => {
    // هنا ممكن نضيف Validation مستقبلاً
    setStep(2);
  };

  return (
    <div className="p-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <h2 className="text-xl font-semibold mb-6 text-slate-900 dark:text-white">
        Business & Ownership Profile
      </h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">SME ID</label>
          <input 
            type="number"
            placeholder="Enter SME identifier"
            className="w-full bg-slate-50 dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-md px-4 py-2.5 focus:ring-2 focus:ring-blue-600 outline-none transition-all"
            value={smeData.sme_id ?? ''}
            onChange={(e) => updateSmeData({ sme_id: Number(e.target.value) })}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Legal Company Name</label>
          <input 
            type="text" 
            placeholder="e.g. TechFlow Solutions"
            className="w-full bg-slate-50 dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-md px-4 py-2.5 focus:ring-2 focus:ring-blue-600 outline-none transition-all"
            value={smeData.legal_name || ''}
            onChange={(e) => updateSmeData({ legal_name: e.target.value })}
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Industry Sector</label>
          <select 
            className="w-full bg-slate-50 dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-md px-4 py-2.5 focus:ring-2 focus:ring-blue-600 outline-none"
            value={smeData.industry || ''}
            onChange={(e) => updateSmeData({ industry: e.target.value })}
          >
            <option value="">Select Industry...</option>
            <option value="Technology">Technology & IT</option>
            <option value="Manufacturing">Manufacturing</option>
            <option value="Retail">Retail & E-commerce</option>
            <option value="Construction">Construction</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Business Age (Months)</label>
          <input 
            type="number" 
            className="w-full bg-slate-50 dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-md px-4 py-2.5 focus:ring-2 focus:ring-blue-600 outline-none"
            value={smeData.business_age_months || ''}
            onChange={(e) => updateSmeData({ business_age_months: Number(e.target.value) })}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Owner Credit Score (300-850)</label>
          <input 
            type="number" 
            className="w-full bg-slate-50 dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-md px-4 py-2.5 focus:ring-2 focus:ring-blue-600 outline-none"
            value={smeData.owner_credit_score || ''}
            onChange={(e) => updateSmeData({ owner_credit_score: Number(e.target.value) })}
          />
        </div>
      </div>

      <div className="flex justify-end mt-10">
        <button 
          onClick={handleNext}
          className="px-6 py-2.5 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors font-medium"
        >
          Next: Financials
        </button>
      </div>
    </div>
  );
}