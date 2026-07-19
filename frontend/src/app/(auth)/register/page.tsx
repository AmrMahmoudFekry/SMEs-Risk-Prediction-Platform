'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  Landmark,
  Lock,
  Mail,
  Loader2,
  UserPlus,
  Building2,
  KeyRound,
  ArrowRight,
} from 'lucide-react';
import { apiClient } from '@/lib/api-client';
import { getErrorMessage } from '@/lib/get-error-message';

type Mode = 'create' | 'join';

const inputClass =
  'w-full rounded-lg border border-slate-700 bg-slate-950/60 px-3 py-2.5 text-sm text-slate-100 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20';

export default function RegisterPage() {
  const [mode, setMode] = useState<Mode>('create');

  return (
    <div className="min-h-screen bg-[#020617] flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        <div className="flex items-center gap-3 justify-center mb-8">
          <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
            <Landmark className="text-white w-5 h-5" />
          </div>
          <span className="font-semibold text-lg text-white tracking-tight">
            SME Risk <span className="text-blue-500">Engine</span>
          </span>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-8 shadow-2xl shadow-black/40">
          <div className="mb-6 grid grid-cols-2 gap-1 rounded-lg bg-slate-950 p-1">
            <TabButton active={mode === 'create'} onClick={() => setMode('create')}>
              Create institution
            </TabButton>
            <TabButton active={mode === 'join'} onClick={() => setMode('join')}>
              Join with code
            </TabButton>
          </div>

          {mode === 'create' ? <CreateOrganizationForm /> : <JoinOrganizationForm />}

          <p className="mt-6 text-center text-sm text-slate-400">
            Already have an account?{' '}
            <a href="/login" className="font-medium text-blue-400 hover:text-blue-300">
              Sign in
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}

function TabButton({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`rounded-md py-2 text-sm font-medium transition ${
        active ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-slate-200'
      }`}
    >
      {children}
    </button>
  );
}

function CreateOrganizationForm() {
  const [organizationName, setOrganizationName] = useState('');
  const [adminName, setAdminName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [tenantCode, setTenantCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await apiClient.post('/auth/register-organization', {
        organization_name: organizationName,
        admin_name: adminName,
        admin_email: email,
        admin_password: password,
      });

      localStorage.setItem('access_token', response.data.access_token);
      setTenantCode(response.data.tenant_code);
      setTimeout(() => router.push('/executive'), 1800);
    } catch (err: any) {
      setError(getErrorMessage(err, 'Could not create your institution.'))
    } finally {
      setIsLoading(false);
    }
  };

  if (tenantCode) {
    return (
      <div className="space-y-4 text-center py-4">
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-emerald-500/10">
          <Building2 className="h-6 w-6 text-emerald-400" />
        </div>
        <p className="text-sm text-slate-300">Institution created. Share this code so teammates can join:</p>
        <p className="font-mono text-lg tracking-widest text-blue-400 bg-slate-950 border border-slate-800 rounded-lg py-3">
          {tenantCode}
        </p>
        <p className="text-xs text-slate-500">Redirecting to your dashboard…</p>
      </div>
    );
  }

  return (
    <form className="space-y-5" onSubmit={handleSubmit}>
      <TextField label="Institution name" icon={<Building2 size={16} />}>
        <input
          required
          value={organizationName}
          onChange={(e) => setOrganizationName(e.target.value)}
          placeholder="National Trust Bank"
          className={inputClass}
        />
      </TextField>

      <TextField label="Your full name" icon={<UserPlus size={16} />}>
        <input
          required
          value={adminName}
          onChange={(e) => setAdminName(e.target.value)}
          placeholder="Sara Ahmed"
          className={inputClass}
        />
      </TextField>

      <TextField label="Work email" icon={<Mail size={16} />}>
        <input
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="sara@institution.com"
          className={inputClass}
        />
      </TextField>

      <TextField label="Password" icon={<Lock size={16} />}>
        <input
          type="password"
          required
          minLength={8}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="At least 8 characters"
          className={inputClass}
        />
      </TextField>

      {error && (
        <div className="rounded-lg border border-red-500/20 bg-red-500/10 px-4 py-2.5 text-sm text-red-300">
          {error}
        </div>
      )}

      <SubmitButton isLoading={isLoading} label="Create institution" />
      <p className="text-xs text-slate-500 text-center">
        You&apos;ll be the first administrator and can invite your team afterwards.
      </p>
    </form>
  );
}

function JoinOrganizationForm() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [tenantCode, setTenantCodeInput] = useState('');
  const [roleName, setRoleName] = useState('Analyst');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await apiClient.post('/auth/register', {
        name,
        email,
        password,
        tenant_code: tenantCode.trim().toUpperCase(),
        role_name: roleName,
      });

      localStorage.setItem('access_token', response.data.access_token);
      router.push('/executive');
    } catch (err: any) {
      setError(getErrorMessage(err, 'Could not join this institution.'));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form className="space-y-5" onSubmit={handleSubmit}>
      <TextField label="Institution code" icon={<KeyRound size={16} />}>
        <input
          required
          value={tenantCode}
          onChange={(e) => setTenantCodeInput(e.target.value)}
          placeholder="Given by your admin, e.g. NATIONAL-TRUST-4F2A"
          className={`${inputClass} uppercase placeholder:normal-case`}
        />
      </TextField>

      <TextField label="Full name" icon={<UserPlus size={16} />}>
        <input required value={name} onChange={(e) => setName(e.target.value)} placeholder="Omar Khaled" className={inputClass} />
      </TextField>

      <TextField label="Work email" icon={<Mail size={16} />}>
        <input
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="omar@institution.com"
          className={inputClass}
        />
      </TextField>

      <TextField label="Password" icon={<Lock size={16} />}>
        <input
          type="password"
          required
          minLength={8}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="At least 8 characters"
          className={inputClass}
        />
      </TextField>

      <TextField label="Role" icon={<UserPlus size={16} />}>
        <select value={roleName} onChange={(e) => setRoleName(e.target.value)} className={inputClass}>
          <option value="Analyst">Analyst</option>
          <option value="Manager">Manager</option>
        </select>
      </TextField>

      {error && (
        <div className="rounded-lg border border-red-500/20 bg-red-500/10 px-4 py-2.5 text-sm text-red-300">
          {error}
        </div>
      )}

      <SubmitButton isLoading={isLoading} label="Join institution" />
    </form>
  );
}

function TextField({ label, icon, children }: { label: string; icon: React.ReactNode; children: React.ReactNode }) {
  return (
    <label className="block">
      <span className="mb-1.5 flex items-center gap-1.5 text-sm font-medium text-slate-300">
        {icon}
        {label}
      </span>
      {children}
    </label>
  );
}

function SubmitButton({ isLoading, label }: { isLoading: boolean; label: string }) {
  return (
    <button
      type="submit"
      disabled={isLoading}
      className="group flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 py-2.5 text-sm font-medium text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-70"
    >
      {isLoading ? (
        <Loader2 className="h-4 w-4 animate-spin" />
      ) : (
        <>
          {label}
          <ArrowRight className="h-4 w-4 transition group-hover:translate-x-0.5" />
        </>
      )}
    </button>
  );
}