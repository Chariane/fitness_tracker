import { apiClient } from './client';
import type { User } from './users';

export interface Prestataire {
  id: number;
  user_id: number;
  business_name: string;
  description: string | null;
  city: string | null;
  verified: boolean;
  verified_at: string | null;
  category_id?: number | null;          // ← ajouté
  proposed_category?: string | null;
  whatsapp?: string | null;
  business_image_url?: string | null;
  map_url?: string | null;
}

export interface VerificationDocument {
  id: number;
  prestataire_id: number;
  document_url: string;
  document_type: string | null;
  status: 'pending' | 'approved' | 'rejected';
  reviewed_at: string | null;
}

export interface ServiceCategory {
  id: number;
  name: string;
}

export interface AdminStats {
  totalUsers: number;
  totalClients: number;
  totalPrestataires: number;
  totalCeremonies: number;
  pendingVerifications: number;
}

export const adminApi = {
  getPendingPrestataires: () => apiClient.get<Prestataire[]>('/admin/prestataires/pending'),
  getPrestataireDocuments: (prestataireId: number) =>
    apiClient.get<VerificationDocument[]>(`/admin/prestataires/${prestataireId}/documents`),
  verifyPrestataire: (prestataireId: number, approved: boolean, comment?: string) =>
    apiClient.post(`/admin/prestataires/${prestataireId}/verify`, { approved, comment }),
  getServiceCategories: () => apiClient.get<ServiceCategory[]>('/service-categories'),
  createServiceCategory: (data: { name: string }) =>
    apiClient.post<ServiceCategory>('/service-categories', data),
  updateServiceCategory: (id: number, data: { name: string }) =>
    apiClient.put<ServiceCategory>(`/service-categories/${id}`, data),
  deleteServiceCategory: (id: number) => apiClient.delete(`/service-categories/${id}`),
  getDashboardStats: () => apiClient.get<AdminStats>('/admin/stats'),
  getUsers: () => apiClient.get<User[]>('/admin/users'),
  toggleUserActive: (userId: number, active: boolean) =>
    apiClient.patch(`/admin/users/${userId}/toggle-active`, { active }),
};