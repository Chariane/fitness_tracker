import { apiClient } from './client';

export interface Ceremony {
  id: number;
  title: string;
  event_date: string;
  location: string | null;
  budget: number | null;
  guest_count: number | null;
  status: string;
  created_at: string;
}

export interface CreateCeremonyData {
  ceremony_type_id: number;
  title: string;
  event_date: string;
  location?: string;
  budget?: number;
  guest_count?: number;
}

export const ceremoniesApi = {
  getAll: () => apiClient.get<Ceremony[]>('/ceremonies'),
  getOne: (id: number) => apiClient.get<Ceremony>(`/ceremonies/${id}`),
  create: (data: CreateCeremonyData) => apiClient.post('/ceremonies', data),
  getSuggestions: (id: number) => apiClient.get(`/ceremonies/${id}/suggestions`),
};