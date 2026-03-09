import { apiClient } from './client';

export interface Prestataire {
  id: number;
  business_name: string;
  description: string | null;
  city: string | null;
  verified: boolean;
  category_id?: number | null;
  created_at: string;
  whatsapp?: string | null;
  business_image_url?: string | null;
  avatar_url?: string | null;
  map_url?: string | null;
}

export interface Offer {
  id: number;
  title: string;
  description: string | null;
  base_price: number | null;
  ceremony_type_id: number;
  is_active: boolean;
  created_at: string;
  views?: number;
  contacts?: number;
}

export interface Review {
  id: number;
  rating: number;
  comment: string | null;
  created_at: string;
  author?: string;
  avatar?: string;
  eventType?: string;
}

export interface PrestataireSearchResult {
  id: number;
  business_name: string;
  category_id?: number | null;
  description: string | null;
  city: string | null;
  verified: boolean;
  whatsapp?: string | null;
  business_image_url?: string | null;
  map_url?: string | null;
  total_offers: number;
  min_price: number | null;
  max_price: number | null;
  avatar_url?: string | null;
  avg_rating: number | null;
  total_reviews: number;
}

export const prestatairesApi = {
  getMyProfile: () => apiClient.get<Prestataire>('/prestataires/me'),
  getPrestataire: (id: number) => apiClient.get<Prestataire>(`/prestataires/${id}`),
  updateProfile: (data: Partial<Omit<Prestataire, 'id' | 'created_at' | 'verified' | 'category_id'>>) =>
    apiClient.put('/prestataires/me', data),
  getOffers: (prestataireId?: number) => {
    const url = prestataireId ? `/offers?prestataire_id=${prestataireId}` : '/offers';
    return apiClient.get<Offer[]>(url);
  },
  createOffer: (data: any) => apiClient.post('/offers', data),
  updateOffer: (id: number, data: any) => apiClient.put(`/offers/${id}`, data),
  deleteOffer: (id: number) => apiClient.delete(`/offers/${id}`),
  getReviews: (prestataireId: number) => apiClient.get<Review[]>(`/reviews/prestataire/${prestataireId}`),
  search: (params: {
    q?: string;
    category_ids?: number[];   // ← modifié : tableau d'IDs
    city?: string;
    min_price?: number;
    max_price?: number;
    verified_only?: boolean;
    sort_by?: string;
    page?: number;
    limit?: number;
  }) => apiClient.get<PrestataireSearchResult[]>('/prestataires/search', { params }),
};