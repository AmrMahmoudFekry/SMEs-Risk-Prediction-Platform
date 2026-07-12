'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { ActivitySquare, UserPlus, Mail, Lock, BuildingOffice2, ShieldCheck } from 'lucide-react';
import { apiClient } from '@/lib/api-client';

export default function RegisterPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [organizationId, setOrganizationId] = useState('1');
  const [roleName, setRoleName] = useState('Analyst');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleRegister = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await apiClient.post('/auth/register', {
        name,
        email,
        password,
        organization_id: Number(organizationId),
        role_name: roleName,
      });

      localStorage.setItem('access_token', response.data.access_token);
      setSuccess('Account created successfully. Redirecting...');
      setTimeout(() => router.push('/executive'), 1000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center px-4 py-12 text-slate-100">
      <div className="w-full max-w-2xl">
        <div className="mb-10 rounded-[2rem] border border-slate-800 bg-slate-900/95 p-10 shadow-2xl shadow-slate-950/40">
          <div className="flex items-center gap-4 mb-8">
            <div className="flex h-14 w-14 items-center justify-center rounded-3xl bg-blue-600 text-white">
              <ActivitySquare className="h-6 w-6" />
            </div>
            <div>
              <p className="text-sm uppercase tracking-[0.3em] text-blue-400">Enterprise registration</p>
              <h1 className="mt-3 text-3xl font-semibold text-white">Create your risk platform account</h1>
            </div>
          </div>

          <form className="space-y-6" onSubmit={handleRegister}>
            <div className="grid gap-6 md:grid-cols-2">
              <Field label="Full name" icon={<UserPlus size={18} />}>
                <input
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full rounded-3xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  placeholder="Sara Ahmed"
                />
              </Field>

              <Field label="Email address" icon={<Mail size={18} />}>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full rounded-3xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  placeholder="sara@example.com"
                />
              </Field>
            </div>

            <div className="grid gap-6 md:grid-cols-2">
              <Field label="Password" icon={<Lock size={18} />}>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full rounded-3xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  placeholder="Enter a strong password"
                />
              </Field>

              <Field label="Organization ID" icon={<BuildingOffice2 size={18} />}>
                <input
                  type="number"
                  required
                  value={organizationId}
                  onChange={(e) => setOrganizationId(e.target.value)}
                  className="w-full rounded-3xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  placeholder="1"
                />
              </Field>
            </div>

            <Field label="Role" icon={<ShieldCheck size={18} />}>
              <select
                value={roleName}
                onChange={(e) => setRoleName(e.target.value)}
                className="w-full rounded-3xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
              >
                <option value="Analyst">Analyst</option>
                <option value="Manager">Manager</option>
              </select>
            </Field>

            {error && (
              <div className="rounded-3xl bg-red-500/10 px-4 py-3 text-sm text-red-300 border border-red-500/20">
                {error}
              </div>
            )}
            {success && (
              <div className="rounded-3xl bg-emerald-500/10 px-4 py-3 text-sm text-emerald-200 border border-emerald-500/20">
                {success}
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="w-full rounded-3xl bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {isLoading ? 'Creating account...' : 'Create account'}
            </button>
          </form>

          <div className="mt-6 flex items-center justify-between text-sm text-slate-400">
            <p>Already registered?</p>
            <a href="/login" className="font-semibold text-blue-400 hover:text-blue-300">Sign in</a>
          </div>
        </div>
      </div>
    </div>
  );
}

function Field({ label, icon, children }: { label: string; icon: React.ReactNode; children: React.ReactNode }) {
  return (
    <label className="block">
      <span className="mb-2 flex items-center gap-2 text-sm font-medium text-slate-300">{icon} {label}</span>
      {children}
    </label>
  );
}
