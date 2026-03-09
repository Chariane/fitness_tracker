import { apiClient } from './client';
import type { Prestataire } from './prestataires';
import type { Offer } from './offers';

export interface PackOfferDetail {
  offer: Offer;
  prestataire: Prestataire;
  category_name: string | null;
  individual_score: number;
}

export interface PackRecommendation {
  offers: PackOfferDetail[];
  total_price: number;
  average_score: number;
  budget_score: number;
  final_score: number;
}

export const packRecommendationsApi = {
  getPacks: (params: {
    ceremony_type_id: number;
    total_budget: number;
    city: string;
    event_date: string;
    guest_count?: number;
  }) => apiClient.post<PackRecommendation[]>('/pack-recommendations', params),
};