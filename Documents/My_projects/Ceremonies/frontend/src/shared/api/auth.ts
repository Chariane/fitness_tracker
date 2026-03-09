import { apiClient } from './client';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: number;
  email: string;
  full_name: string | null;
  is_active: boolean;
  is_client: boolean;
  is_prestataire: boolean;
  is_admin: boolean;
  created_at: string;
  avatar_url?: string | null;
}

export const authApi = {
  login: (credentials: LoginCredentials) =>
    apiClient.post<AuthResponse>('/auth/login', credentials),

  register: (data: RegisterData) =>
    apiClient.post('/auth/register', data),

  getCurrentUser: () =>
    apiClient.get<User>('/users/me'),

  becomePrestataire: (profileData: any) =>
    apiClient.post('/prestataires/request', profileData),
};