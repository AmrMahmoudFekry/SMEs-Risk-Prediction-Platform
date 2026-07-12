'use client';

import { useState, useEffect } from 'react';
import { Download, Search, Loader2 } from 'lucide-react';
import { apiClient } from '@/lib/api-client';

export default function ReportsHub() {
  const [searchTerm, setSearchTerm] = useState('');
  const [reports, setReports] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const response = await apiClient.get('/reports/history');
        setReports(response.data);
      } catch (error) {
        console.error('Failed to fetch reports', error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchReports();
  }, []);

  const handleDownload = async (assessmentId: number) => {
    try {
      const genResponse = await apiClient.post(`/reports/generate/${assessmentId}`);
      const downloadUrl = genResponse.data.download_url || genResponse.data.file_url;
      if (downloadUrl) {
        window.open(downloadUrl, '_blank');
      } else {
        alert('Report generated successfully, but no download URL was returned.');
      }
    } catch (error) {
      alert('Error generating or downloading report.');
    }
  };

  const filteredReports = reports.filter((r) =>
    r.smeName?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    String(r.db_id).toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-full px-8 py-8">
      <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Reporting Portal</p>
          <h1 className="mt-3 text-4xl font-semibold text-white">AI Generated Risk Reports</h1>
          <p className="mt-3 max-w-2xl text-slate-400">View the latest report outputs, filter by SME, and download the documents you need.</p>
        </div>
        <div className="relative w-full max-w-md">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
          <input
            type="text"
            placeholder="Search by SME name or report ID"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full rounded-3xl border border-slate-800 bg-slate-950/80 px-12 py-3 text-slate-100 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
          />
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.05fr_0.75fr]">
        <div className="rounded-3xl border border-slate-800 bg-slate-950/80 p-6 shadow-[0_25px_60px_rgba(15,23,42,0.35)]">
          <h2 className="text-xl font-semibold text-white mb-4">Latest generated reports</h2>
          {isLoading ? (
            <div className="flex h-64 items-center justify-center">
              <Loader2 className="animate-spin h-10 w-10 text-blue-500" />
            </div>
          ) : (
            <div className="space-y-4">
              {filteredReports.slice(0, 6).map((report) => (
                <div key={report.id} className="rounded-3xl border border-slate-800 bg-slate-900/80 p-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <p className="text-sm text-slate-400">{report.smeName}</p>
                    <p className="mt-1 text-lg font-semibold text-white">Report {report.id}</p>
                    <p className="text-xs text-slate-500 mt-1">{report.date} • {report.risk}</p>
                  </div>
                  <button
                    onClick={() => handleDownload(report.db_id)}
                    className="inline-flex items-center justify-center rounded-3xl bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-500 transition"
                  >
                    Download
                  </button>
                </div>
              ))}
              {filteredReports.length === 0 && (
                <div className="rounded-3xl border border-dashed border-slate-700 bg-slate-900/80 p-8 text-center text-slate-500">
                  No reports match your search.
                </div>
              )}
            </div>
          )}
        </div>

        <aside className="rounded-3xl border border-slate-800 bg-slate-950/80 p-6 shadow-[0_25px_60px_rgba(15,23,42,0.35)]">
          <h2 className="text-xl font-semibold text-white mb-4">Summary</h2>
          <div className="space-y-4">
            <StatTile label="Total reports" value={String(reports.length)} />
            <StatTile label="High risk" value="24" />
            <StatTile label="Avg confidence" value="92.4%" />
          </div>
          <div className="mt-6 rounded-3xl border border-slate-800 bg-slate-900/80 p-4">
            <p className="text-sm text-slate-400">Export a CSV of all risk report results for compliance review.</p>
            <button className="mt-4 w-full rounded-3xl bg-slate-800 px-5 py-3 text-sm font-semibold text-white hover:bg-slate-700 transition">Export history</button>
          </div>
        </aside>
      </div>
    </div>
  );
}

function StatTile({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-5">
      <p className="text-sm text-slate-400">{label}</p>
      <p className="mt-3 text-3xl font-semibold text-white">{value}</p>
    </div>
  );
}
