'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Landmark, Lock, Mail, Loader2, ShieldCheck, ArrowRight } from 'lucide-react';
import { apiClient } from '@/lib/api-client';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  useEffect(() => {
    if (typeof window !== 'undefined' && localStorage.getItem('access_token')) {
      router.replace('/executive');
    }
  }, [router]);

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const response = await apiClient.post('/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });

      localStorage.setItem('access_token', response.data.access_token);
      router.push('/executive');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Invalid credentials. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#020617] flex">
      {/* Left panel — brand & signature visual, hidden on small screens */}
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden border-r border-slate-800/80 flex-col justify-between p-12">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-600/10 via-transparent to-transparent" />

        <div className="relative flex items-center gap-3">
          <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
            <Landmark className="text-white w-5 h-5" />
          </div>
          <span className="font-semibold text-lg text-white tracking-tight">
            SME Risk <span className="text-blue-500">Engine</span>
          </span>
        </div>

        <div className="relative">
          <h1 className="text-4xl font-semibold text-white leading-tight tracking-tight max-w-md">
            Underwrite SME credit risk with model-grade confidence.
          </h1>
          <p className="mt-4 text-slate-400 max-w-sm text-sm leading-relaxed">
            A single console for risk analysts, credit managers, and compliance teams to score,
            explain, and report on every SME exposure across your institution.
          </p>

          <RiskPulseSignature />

          <ul className="mt-8 space-y-3 text-sm text-slate-300">
            <li className="flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-blue-500 shrink-0" />
              Data isolated per institution, enforced on every request
            </li>
            <li className="flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-blue-500 shrink-0" />
              Every score explainable down to the feature level
            </li>
          </ul>
        </div>

        <p className="relative text-xs text-slate-600">© 2026 SME Risk Intelligence Platform</p>
      </div>

      {/* Right panel — form */}
      <div className="flex-1 flex flex-col justify-center px-6 py-12 sm:px-12">
        <div className="mx-auto w-full max-w-sm">
          <div className="lg:hidden flex items-center gap-2 mb-8">
            <div className="w-9 h-9 bg-blue-600 rounded-lg flex items-center justify-center">
              <Landmark className="text-white w-5 h-5" />
            </div>
            <span className="font-semibold text-lg text-white tracking-tight">
              SME Risk <span className="text-blue-500">Engine</span>
            </span>
          </div>

          <h2 className="text-2xl font-semibold text-white tracking-tight">Sign in</h2>
          <p className="mt-1 text-sm text-slate-400">Access your institution&apos;s risk console.</p>

          <form className="mt-8 space-y-5" onSubmit={handleLogin}>
            <div>
              <label className="block text-sm font-medium text-slate-300">Work email</label>
              <div className="mt-1.5 relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
                <input
                  type="email"
                  required
                  autoFocus
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full rounded-lg border border-slate-700 bg-slate-900/60 pl-10 pr-3 py-2.5 text-sm text-slate-100 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  placeholder="you@institution.com"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300">Password</label>
              <div className="mt-1.5 relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full rounded-lg border border-slate-700 bg-slate-900/60 pl-10 pr-3 py-2.5 text-sm text-slate-100 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  placeholder="••••••••"
                />
              </div>
            </div>

            {error && (
              <div className="rounded-lg border border-red-500/20 bg-red-500/10 px-4 py-2.5 text-sm text-red-300">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="group flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 py-2.5 text-sm font-medium text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <>
                  Sign in
                  <ArrowRight className="h-4 w-4 transition group-hover:translate-x-0.5" />
                </>
              )}
            </button>
          </form>

          <p className="mt-8 text-center text-sm text-slate-400">
            New to the platform?{' '}
            <a href="/register" className="font-medium text-blue-400 hover:text-blue-300">
              Set up your institution
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}

function RiskPulseSignature() {
  return (
    <div className="mt-10 h-16 w-full max-w-sm">
      <svg viewBox="0 0 320 64" className="w-full h-full" fill="none">
        <path
          d="M0 40 L30 40 L42 12 L54 52 L66 24 L78 40 L100 40 L112 30 L124 40 L320 40"
          stroke="#3B82F6"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          opacity="0.9"
        >
          <animate
            attributeName="d"
            dur="4s"
            repeatCount="indefinite"
            values="
              M0 40 L30 40 L42 12 L54 52 L66 24 L78 40 L100 40 L112 30 L124 40 L320 40;
              M0 40 L30 40 L42 34 L54 46 L66 32 L78 40 L100 40 L112 37 L124 40 L320 40;
              M0 40 L30 40 L42 12 L54 52 L66 24 L78 40 L100 40 L112 30 L124 40 L320 40
            "
          />
        </path>
        <line x1="124" y1="40" x2="320" y2="40" stroke="#1E293B" strokeWidth="2" />
      </svg>
      <p className="mt-2 text-xs text-slate-500">Model confidence stabilizing in real time</p>
    </div>
  );
}