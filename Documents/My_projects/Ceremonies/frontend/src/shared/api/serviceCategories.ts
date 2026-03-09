import { apiClient } from './client';

export interface ServiceCategory {
  id: number;
  name: string;
  description: string | null;
}

export const serviceCategoriesApi = {
  getAll: () => apiClient.get<ServiceCategory[]>('/service-categories'),
  getOne: (id: number) => apiClient.get<ServiceCategory>(`/service-categories/${id}`),
  create: (data: { name: string }) => 
    apiClient.post<ServiceCategory>('/service-categories', data),
  update: (id: number, data: { name: string }) =>
    apiClient.put<ServiceCategory>(`/service-categories/${id}`, data),
  delete: (id: number) => apiClient.delete(`/service-categories/${id}`),
};