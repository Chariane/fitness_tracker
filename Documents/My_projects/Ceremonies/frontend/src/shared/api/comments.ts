import { apiClient } from './client';

export interface Comment {
  id: number;
  user_id: number;
  offer_id: number;
  content: string;
  created_at: string;
  author_name?: string;
  author_avatar?: string;
}

export const commentsApi = {
  getByOffer: (offerId: number) => apiClient.get<Comment[]>(`/comments?offer_id=${offerId}`),
  create: (data: { offer_id: number; content: string }) => apiClient.post<Comment>('/comments', data),
  delete: (id: number) => apiClient.delete(`/comments/${id}`),
};