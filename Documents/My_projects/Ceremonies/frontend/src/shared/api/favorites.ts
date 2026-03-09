import { apiClient } from './client';

export const favoritesApi = {
  add: (offerId: number) => apiClient.post(`/favorites/${offerId}`),
  remove: (offerId: number) => apiClient.delete(`/favorites/${offerId}`),
  check: (offerId: number) => apiClient.get<{ liked: boolean }>(`/favorites/check/${offerId}`),
};