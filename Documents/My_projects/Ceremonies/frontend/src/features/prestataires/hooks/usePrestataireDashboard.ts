import { useState, useEffect } from 'react';
import { useAuth } from '../../../features/auth/hooks/useAuth';
import { apiClient } from '../../../shared/api/client';
import type { Offer } from '../../../shared/api/prestataires';

interface Request {
  id: number;
  client: string;
  event: string;
  message: string;
  date: string;
}

interface DashboardStats {
  totalViews: number;
  totalContacts: number;
  totalReservations: number;
  averageRating: number;
}

export function usePrestataireDashboard() {
  const { user } = useAuth();
  const [offers, setOffers] = useState<Offer[]>([]);
  const [requests, setRequests] = useState<Request[]>([]);
  const [stats, setStats] = useState<DashboardStats>({
    totalViews: 0,
    totalContacts: 0,
    totalReservations: 0,
    averageRating: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user?.is_prestataire) return;

    const fetchData = async () => {
      try {
        // 1. Récupérer les statistiques
        const statsRes = await apiClient.get('/prestataires/me/dashboard');
        setStats(statsRes.data);

        // 2. Récupérer les offres du prestataire connecté
        const offersRes = await apiClient.get('/offers/me');
        setOffers(offersRes.data);

        // 3. Récupérer les conversations (demandes) – déjà fait via messagesApi
        const convsRes = await apiClient.get('/chat/conversations');
        const recentReqs: Request[] = convsRes.data.slice(0, 3).map((conv: any) => ({
          id: conv.id,
          client: `Client ${conv.client_id}`, // à remplacer par le vrai nom
          event: conv.event_name || 'Événement',
          message: conv.last_message?.content || '',
          date: new Date(conv.updated_at).toLocaleDateString(),
        }));
        setRequests(recentReqs);

      } catch (error) {
        console.error('Erreur chargement dashboard prestataire', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [user]);

  return { offers, requests, stats, loading };
}