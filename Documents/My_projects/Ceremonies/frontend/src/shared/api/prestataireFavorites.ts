import { apiClient } from './client';
import type { Prestataire } from './prestataires';

export const prestataireFavoritesApi = {
  add: (prestataireId: number) => apiClient.post(`/prestataire-favorites/${prestataireId}`),
  remove: (prestataireId: number) => apiClient.delete(`/prestataire-favorites/${prestataireId}`),
  check: (prestataireId: number) => apiClient.get<{ isFavorite: boolean }>(`/prestataire-favorites/check/${prestataireId}`),
  getCount: () => apiClient.get<{ count: number }>('/prestataire-favorites/count'),
  getAll: () => apiClient.get<Prestataire[]>('/prestataire-favorites'),
};