'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api-client';

export type CurrentUser = {
  id: number;
  name: string;
  email: string;
  organization_id: number;
  role: string;
};

export function useAuth() {
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
    if (!token) {
      setIsLoading(false);
      return;
    }

    const fetchUser = async () => {
      try {
        const response = await apiClient.get('/auth/me');
        setUser(response.data);
      } catch (error) {
        localStorage.removeItem('access_token');
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    fetchUser();
  }, []);

  const logout = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      router.push('/login');
    }
  };

  return { user, isLoading, logout };
}
