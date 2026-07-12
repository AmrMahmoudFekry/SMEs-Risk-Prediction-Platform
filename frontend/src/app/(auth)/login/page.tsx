'use client';

'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ActivitySquare, Lock, Mail, Loader2 } from 'lucide-react';
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
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
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
    <div className="min-h-screen bg-slate-50 dark:bg-[#0F172A] flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center items-center gap-2 mb-6">
          <div className="w-10 h-10 bg-blue-600 rounded-md flex items-center justify-center">
            <ActivitySquare className="text-white w-6 h-6" />
          </div>
          <span className="font-bold text-2xl text-slate-900 dark:text-white tracking-tight">
            SME Risk <span className="text-blue-600">Engine</span>
          </span>
        </div>
        <h2 className="text-center text-xl tracking-tight font-medium text-slate-900 dark:text-white">
          Sign in to your enterprise account
        </h2>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white dark:bg-[#1E293B] py-8 px-4 shadow-sm border border-slate-200 dark:border-slate-800 sm:rounded-xl sm:px-10">
          <form className="space-y-6" onSubmit={handleLogin}>
            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">Email address</label>
              <div className="mt-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail className="h-5 w-5 text-slate-400" />
                </div>
                <input
                  type="email" required
                  className="pl-10 block w-full bg-slate-50 dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-md py-2 focus:ring-2 focus:ring-blue-600 outline-none"
                  value={email} onChange={(e) => setEmail(e.target.value)}
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">Password</label>
              <div className="mt-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-slate-400" />
                </div>
                <input
                  type="password" required
                  className="pl-10 block w-full bg-slate-50 dark:bg-[#0F172A] border border-slate-200 dark:border-slate-700 rounded-md py-2 focus:ring-2 focus:ring-blue-600 outline-none"
                  value={password} onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>

            {error && <div className="text-sm text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 p-3 rounded-md">{error}</div>}

            <button
              type="submit" disabled={isLoading}
              className="w-full flex justify-center py-2.5 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-70 transition-colors"
            >
              {isLoading ? <Loader2 className="animate-spin w-5 h-5" /> : 'Sign in'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}