import { apiClient } from './client';

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

export const usersApi = {
  getCurrentUser: () => apiClient.get<User>('/users/me'),
  updateProfile: (data: { full_name?: string }) =>
    apiClient.put<User>('/users/me', data),
  getUserById: (id: number) => apiClient.get<User>(`/users/${id}`),
};