'use client';

import { useEffect, useState } from 'react';
import { useAssessmentStore } from '@/store/useAssessmentStore';
import { apiClient } from '@/lib/api-client';
import { getErrorMessage } from '@/lib/get-error-message';
import { Loader2, Plus } from 'lucide-react';

type SME = {
  id: number;
  legal_name: string;
  industry: string | null;
  business_age_months: number | null;
  status: string;
};

const INDUSTRY_OPTIONS = ['Technology', 'Manufacturing', 'Retail', 'Construction', 'Agriculture', 'Services'];

export default function BusinessInfoStep() {
  const { smeData, updateSmeData, setStep } = useAssessmentStore();
  const [smes, setSmes] = useState<SME[]>([]);
  const [isLoadingSmes, setIsLoadingSmes] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [error, setError] = useState('');

  const [newLegalName, setNewLegalName] = useState('');
  const [newIndustry, setNewIndustry] = useState('');
  const [newBusinessAge, setNewBusinessAge] = useState('');
  const [isCreating, setIsCreating] = useState(false);

  const loadSmes = async () => {
    setIsLoadingSmes(true);
    try {
      const response = await apiClient.get('/smes', { params: { limit: 100 } });
      setSmes(response.data.items);
    } catch (err: any) {
      setError(getErrorMessage(err, 'Could not load your SME list.'));
    } finally {
      setIsLoadingSmes(false);
    }
  };

  useEffect(() => {
    loadSmes();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleSelectSme = (id: string) => {
    const smeId = Number(id);
    const selected = smes.find((s) => s.id === smeId);
    updateSmeData({
      sme_id: smeId,
      legal_name: selected?.legal_name,
      industry: selected?.industry,
      business_age_months: selected?.business_age_months,
    });
  };

  const handleCreateSme = async () => {
    if (!newLegalName.trim()) {
      setError('Legal company name is required.');
      return;
    }
    setIsCreating(true);
    setError('');
    try {
      const response = await apiClient.post('/smes/', {
        legal_name: newLegalName,
        industry: newIndustry || null,
        business_age_months: newBusinessAge ? Number(newBusinessAge) : null,
      });
      const created: SME = response.data;
      setSmes((prev) => [created, ...prev]);
      updateSmeData({
        sme_id: created.id,
        legal_name: created.legal_name,
        industry: created.industry,
        business_age_months: created.business_age_months,
      });
      setShowCreateForm(false);
      setNewLegalName('');
      setNewIndustry('');
      setNewBusinessAge('');
    } catch (err: any) {
      setError(getErrorMessage(err, 'Could not create the SME.'));
    } finally {
      setIsCreating(false);
    }
  };

  const handleNext = () => {
    if (!smeData.sme_id) {
      setError('Please select or create an SME before continuing.');
      return;
    }
    setError('');
    setStep(2);
  };

  return (
    <div className="p-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <h2 className="text-xl font-semibold mb-6 text-slate-900 dark:text-white">
        Business & Ownership Profile
      </h2>

      <div className="mb-8">
        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
          Select SME to assess
        </label>
        {isLoadingSmes ? (
          <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400 py-2.5">
            <Loader2 className="w-4 h-4 animate-spin" /> Loading your SMEs…
          </div>
        ) : (
          <div className="flex gap-3">
            <select
              className="flex-1 bg-slate-50 dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-md px-4 py-2.5 focus:ring-2 focus:ring-blue-600 outline-none"
              value={smeData.sme_id ?? ''}
              onChange={(e) => handleSelectSme(e.target.value)}
            >
              <option value="">Select an SME…</option>
              {smes.map((sme) => (
                <option key={sme.id} value={sme.id}>
                  {sme.legal_name}
                </option>
              ))}
            </select>
            <button
              type="button"
              onClick={() => setShowCreateForm((v) => !v)}
              className="flex items-center gap-1.5 px-4 py-2.5 rounded-md border border-slate-300 dark:border-slate-700 text-sm font-medium text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
            >
              <Plus size={16} /> New SME
            </button>
          </div>
        )}
      </div>

      {showCreateForm && (
        <div className="mb-8 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/40 p-6">
          <h3 className="text-sm font-semibold text-slate-900 dark:text-white mb-4">Create a new SME</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <input
              type="text"
              placeholder="Legal company name"
              value={newLegalName}
              onChange={(e) => setNewLegalName(e.target.value)}
              className="bg-white dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-md px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-blue-600"
            />
            <select
              value={newIndustry}
              onChange={(e) => setNewIndustry(e.target.value)}
              className="bg-white dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-md px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-blue-600"
            >
              <option value="">Industry (optional)</option>
              {INDUSTRY_OPTIONS.map((i) => (
                <option key={i} value={i}>{i}</option>
              ))}
            </select>
            <input
              type="number"
              placeholder="Business age (months)"
              value={newBusinessAge}
              onChange={(e) => setNewBusinessAge(e.target.value)}
              className="bg-white dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-md px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-blue-600"
            />
          </div>
          <div className="mt-4 flex justify-end">
            <button
              type="button"
              onClick={handleCreateSme}
              disabled={isCreating}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 disabled:opacity-70 transition-colors"
            >
              {isCreating && <Loader2 className="w-4 h-4 animate-spin" />}
              Save SME
            </button>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Industry Sector</label>
          <select
            className="w-full bg-slate-50 dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-md px-4 py-2.5 focus:ring-2 focus:ring-blue-600 outline-none"
            value={smeData.industry || ''}
            onChange={(e) => updateSmeData({ industry: e.target.value })}
          >
            <option value="">Select Industry…</option>
            {INDUSTRY_OPTIONS.map((i) => (
              <option key={i} value={i}>{i}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Business Age (Months)</label>
          <input
            type="number"
            className="w-full bg-slate-50 dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-md px-4 py-2.5 focus:ring-2 focus:ring-blue-600 outline-none"
            value={smeData.business_age_months ?? ''}
            onChange={(e) => updateSmeData({ business_age_months: Number(e.target.value) })}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Owner Credit Score (300-850)</label>
          <input
            type="number"
            min={300}
            max={850}
            className="w-full bg-slate-50 dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-md px-4 py-2.5 focus:ring-2 focus:ring-blue-600 outline-none"
            value={smeData.owner_credit_score ?? ''}
            onChange={(e) => updateSmeData({ owner_credit_score: Number(e.target.value) })}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Owner Ownership Percentage (%)</label>
          <input
            type="number"
            min={0}
            max={100}
            className="w-full bg-slate-50 dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-md px-4 py-2.5 focus:ring-2 focus:ring-blue-600 outline-none"
            value={smeData.owner_percentage ?? ''}
            onChange={(e) => updateSmeData({ owner_percentage: Number(e.target.value) })}
          />
        </div>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 text-red-600 dark:bg-red-900/20 dark:text-red-400 rounded-md border border-red-200 dark:border-red-800 text-sm">
          {error}
        </div>
      )}

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