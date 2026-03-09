import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { authApi } from '../../../shared/api/auth';
import type { LoginCredentials, RegisterData, User } from '../../../shared/api/auth';

export function useAuth() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [isInitialized, setIsInitialized] = useState(false);
  const navigate = useNavigate();

  // Charger le profil si token présent
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token && !user) {
      authApi.getCurrentUser()
        .then((res) => {
          setUser(res.data);
        })
        .catch(() => {
          localStorage.removeItem('token');
        })
        .finally(() => {
          setIsInitialized(true);
        });
    } else {
      setIsInitialized(true);
    }
  }, []);

  const login = async (credentials: LoginCredentials) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await authApi.login(credentials);
      localStorage.setItem('token', response.data.access_token);
      const userRes = await authApi.getCurrentUser();
      setUser(userRes.data);
      if (userRes.data.is_admin) {
        navigate('/admin');
      } else if (userRes.data.is_prestataire) {
        navigate('/prestataire/dashboard');
      } else {
        navigate('/dashboard');
      }
    } catch (err) {
      setError('Email ou mot de passe incorrect');
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (data: RegisterData, role: 'client' | 'prestataire') => {
    setIsLoading(true);
    setError(null);
    try {
      await authApi.register(data);
      await login({ email: data.email, password: data.password });
      if (role === 'prestataire') {
        navigate('/become-prestataire');
      }
    } catch (err) {
      setError("Erreur lors de l'inscription");
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    navigate('/');
  };

  return { login, register, logout, isLoading, error, user, setUser, isInitialized };
}