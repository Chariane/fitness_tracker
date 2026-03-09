import { apiClient } from './client';

export interface Offer {
  id: number;
  title: string;
  prestataire_id: number;
  description: string | null;
  base_price: number | null;
  ceremony_type_id: number;  // ← modifié
  is_active: boolean;
  likes_count?: number;
  created_at: string;
  views?: number;
  contacts?: number;
}

export interface CreateOfferData {
  ceremony_type_id: number;  // ← modifié
  title: string;
  description?: string | null;
  base_price?: number | null;
}

export const offersApi = {
  getMyOffers: () => apiClient.get<Offer[]>('/offers/me'),
  getAll: () => apiClient.get<Offer[]>('/offers'),
  create: (data: CreateOfferData) => apiClient.post<Offer>('/offers', data),
  getOne: (id: number) => apiClient.get<Offer>(`/offers/${id}`),
  update: (id: number, data: CreateOfferData) => apiClient.put<Offer>(`/offers/${id}`, data),
  delete: (id: number) => apiClient.delete(`/offers/${id}`),
};