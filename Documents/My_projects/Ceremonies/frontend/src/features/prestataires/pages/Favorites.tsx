// src/features/prestataires/pages/Favorites.tsx
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  HeartIcon as HeartSolid,
  MapPinIcon,
  ShieldCheckIcon,
} from '@heroicons/react/24/solid';
import { Container } from '../../../shared/components/ui/Container';
import { Card } from '../../../shared/components/ui/Card';
import { Button } from '../../../shared/components/ui/Button';
import { Avatar } from '../../../shared/components/ui/Avatar';
import { prestataireFavoritesApi } from '../../../shared/api/prestataireFavorites';
import type { Prestataire } from '../../../shared/api/prestataires';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function Favorites() {
  const navigate = useNavigate();
  const [prestataires, setPrestataires] = useState<Prestataire[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchFavorites();
  }, []);

  const fetchFavorites = async () => {
    try {
      const res = await prestataireFavoritesApi.getAll();
      setPrestataires(res.data);
    } catch (err) {
      console.error('Erreur chargement favoris', err);
      setError('Impossible de charger vos favoris.');
    } finally {
      setLoading(false);
    }
  };

  const handleRemove = async (prestataireId: number) => {
    try {
      await prestataireFavoritesApi.remove(prestataireId);
      setPrestataires(prev => prev.filter(p => p.id !== prestataireId));
    } catch (err) {
      console.error('Erreur suppression favori', err);
      alert('Impossible de retirer des favoris.');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background pt-24 flex justify-center">
        <div className="w-12 h-12 border-4 border-primary-200 border-t-primary-500 rounded-full animate-spin" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background pt-24 text-center">
        <p className="text-text-secondary">{error}</p>
        <Button variant="primary" onClick={() => navigate('/')} className="mt-4">
          Retour à l'accueil
        </Button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background pt-24 pb-16">
      <Container>
        <h1 className="text-3xl md:text-4xl font-bold text-text-primary mb-8">
          Mes prestataires favoris
        </h1>

        {prestataires.length === 0 ? (
          <div className="text-center py-12">
            <HeartSolid className="w-16 h-16 text-text-tertiary mx-auto mb-4" />
            <p className="text-text-secondary mb-4">Vous n'avez aucun prestataire favori pour le moment.</p>
            <Button variant="primary" onClick={() => navigate('/search')}>
              Découvrir des prestataires
            </Button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {prestataires.map((prestataire, index) => (
              <motion.div
                key={prestataire.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
              >
                <Card className="p-6 hover:shadow-medium transition-all duration-300">
                  <div className="flex items-start gap-4 mb-4">
                    <Avatar
                      src={prestataire.avatar_url ? `${API_URL}${prestataire.avatar_url}` : undefined}
                      initials={prestataire.business_name.charAt(0)}
                      size="md"
                    />
                    <div className="flex-1">
                      <h3 className="font-bold text-text-primary text-lg">{prestataire.business_name}</h3>
                      <p className="text-text-secondary text-sm line-clamp-2">{prestataire.description}</p>
                    </div>
                  </div>

                  <div className="space-y-2 mb-4">
                    <div className="flex items-center gap-2 text-sm text-text-secondary">
                      <MapPinIcon className="w-4 h-4" />
                      <span>{prestataire.city || "Localisation non renseignée"}</span>
                    </div>
                    {prestataire.verified && (
                      <div className="flex items-center gap-2 text-sm text-green-600">
                        <ShieldCheckIcon className="w-4 h-4" />
                        <span>Prestataire vérifié</span>
                      </div>
                    )}
                  </div>

                  <div className="flex gap-2">
                    <Button
                      variant="primary"
                      fullWidth
                      onClick={() => navigate(`/prestataire/${prestataire.id}`)}
                    >
                      Voir le profil
                    </Button>
                    <Button
                      variant="outline"
                      onClick={() => handleRemove(prestataire.id)}
                      className="px-3"
                      title="Retirer des favoris"
                    >
                      <HeartSolid className="w-5 h-5 text-red-500" />
                    </Button>
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        )}
      </Container>
    </div>
  );
}