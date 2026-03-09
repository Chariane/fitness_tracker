import { apiClient } from './client';

export interface OfferMedia {
  id: number;
  media_url: string;
  media_type: string | null;
  created_at: string;
}

export const offerMediaApi = {
  // Récupérer les médias d'une offre
  getByOffer: (offerId: number) => apiClient.get<OfferMedia[]>(`/offer-media/${offerId}`),

  // Uploader un média
  upload: (offerId: number, file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return apiClient.post<OfferMedia>(`/offer-media/upload/${offerId}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  // Supprimer un média
  delete: (mediaId: number) => apiClient.delete(`/offer-media/${mediaId}`),
};