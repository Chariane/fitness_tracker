import { apiClient } from './client';

export interface CeremonyType {
  id: number;
  name: string;
  description: string | null;
}

export const ceremonyTypesApi = {
  getAll: () => apiClient.get<CeremonyType[]>('/ceremony-types'),
  getOne: (id: number) => apiClient.get<CeremonyType>(`/ceremony-types/${id}`),
  create: (data: { name: string; description?: string }) => 
    apiClient.post<CeremonyType>('/ceremony-types', data),
  update: (id: number, data: { name: string; description?: string }) =>
    apiClient.put<CeremonyType>(`/ceremony-types/${id}`, data),
  delete: (id: number) => apiClient.delete(`/ceremony-types/${id}`),
};