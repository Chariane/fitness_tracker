import { apiClient } from './client';
import type { Offer } from './offers';
import type { Prestataire } from './prestataires';

export interface Pack {
  id: number;
  user_id: number;
  event_id?: number | null;
  name: string;
  user_budget?: number | null;
  total_price: number;
  completion_score: number;
  created_at: string;
  offers: PackOffer[];
}

export interface PackOffer {
  id: number;
  pack_id: number;
  offer_id: number;
  added_at: string;
  offer: Offer;
}

export interface CreatePackData {
  name: string;
  event_id?: number | null;
  user_budget?: number | null;
  offer_ids: number[];
}

export interface UpdatePackData {
  name?: string;
  offer_ids?: number[];
  user_budget?: number | null;
}

export const packsApi = {
  // Créer un nouveau pack
  create: (data: CreatePackData) => apiClient.post<Pack>('/packs', data),

  // Lister les packs de l'utilisateur connecté
  getMyPacks: () => apiClient.get<Pack[]>('/packs'),

  // Récupérer un pack par son ID
  getOne: (id: number) => apiClient.get<Pack>(`/packs/${id}`),

  // Mettre à jour un pack
  update: (id: number, data: UpdatePackData) => apiClient.put<Pack>(`/packs/${id}`, data),

  // Supprimer un pack
  delete: (id: number) => apiClient.delete(`/packs/${id}`),
};