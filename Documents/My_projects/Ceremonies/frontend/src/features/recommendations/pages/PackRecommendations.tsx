import { useState, useEffect } from "react";
import { useNavigate, useSearchParams, Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  CurrencyEuroIcon,
  UserIcon,
  StarIcon,
  MapPinIcon,
  ShieldCheckIcon,
  SparklesIcon,
  CheckCircleIcon,
  XCircleIcon,
} from "@heroicons/react/24/outline";
import { StarIcon as StarIconSolid } from "@heroicons/react/24/solid";
import { Container } from "../../../shared/components/ui/Container";
import { Card } from "../../../shared/components/ui/Card";
import { Button } from "../../../shared/components/ui/Button";
import { Avatar } from "../../../shared/components/ui/Avatar";
import { packRecommendationsApi } from "../../../shared/api/packRecommendations";
import type { PackRecommendation } from "../../../shared/api/packRecommendations";

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function PackRecommendations() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [packs, setPacks] = useState<PackRecommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const ceremony_type_id = searchParams.get('ceremony_type_id');
  const total_budget = searchParams.get('total_budget');
  const city = searchParams.get('city');
  const event_date = searchParams.get('event_date');
  const guest_count = searchParams.get('guest_count');

  useEffect(() => {
    if (!ceremony_type_id || !total_budget || !city || !event_date) {
      navigate('/event-builder');
      return;
    }

    const fetchPacks = async () => {
      try {
        const res = await packRecommendationsApi.getPacks({
          ceremony_type_id: parseInt(ceremony_type_id),
          total_budget: parseFloat(total_budget),
          city,
          event_date,
          guest_count: guest_count ? parseInt(guest_count) : undefined,
        });
        setPacks(res.data);
      } catch (err) {
        console.error("Erreur chargement packs", err);
        setError("Impossible de charger les packs recommandés.");
      } finally {
        setLoading(false);
      }
    };
    fetchPacks();
  }, [ceremony_type_id, total_budget, city, event_date, guest_count, navigate]);

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
        <Button variant="primary" onClick={() => navigate('/event-builder')} className="mt-4">
          Retour au formulaire
        </Button>
      </div>
    );
  }

  const formatPrice = (price: number) => `${price.toFixed(0)}€`;

  return (
    <div className="min-h-screen bg-background pt-24 pb-16">
      <Container>
        <div className="flex items-center gap-2 text-text-secondary mb-6">
          <button onClick={() => navigate(-1)} className="hover:text-primary-500">
            ← Retour
          </button>
        </div>

        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold text-text-primary mb-2">
              Packs événementiels recommandés
            </h1>
            <p className="text-text-secondary text-lg flex items-center gap-2">
              <SparklesIcon className="w-5 h-5 text-gold-500" />
              Des combinaisons d'offres optimisées pour votre événement
            </p>
          </div>
          <Button variant="outline" onClick={() => navigate('/event-builder')}>
            Modifier mes critères
          </Button>
        </div>

        {packs.length === 0 ? (
          <p className="text-text-secondary text-center py-12">
            Aucun pack ne correspond à vos critères. Essayez d'élargir votre recherche.
          </p>
        ) : (
          <div className="space-y-6">
            {packs.map((pack, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="p-6 hover:shadow-medium transition-all duration-300">
                  <div className="flex flex-wrap justify-between items-start gap-4 mb-4">
                    <div>
                      <h2 className="text-xl font-bold text-text-primary mb-1">
                        Pack #{index + 1}
                      </h2>
                      <div className="flex flex-wrap gap-4 text-sm">
                        <span className="flex items-center gap-1 text-primary-500 font-medium">
                          <CurrencyEuroIcon className="w-4 h-4" />
                          Total : {formatPrice(pack.total_price)}
                        </span>
                        <span className="flex items-center gap-1 text-gold-500">
                          <StarIconSolid className="w-4 h-4" />
                          Score qualité : {pack.average_score.toFixed(2)}
                        </span>
                        <span className="flex items-center gap-1 text-green-600">
                          <CheckCircleIcon className="w-4 h-4" />
                          Adéquation budget : {pack.budget_score.toFixed(2)}
                        </span>
                        <span className="flex items-center gap-1 text-primary-500 font-bold">
                          Score final : {pack.final_score.toFixed(2)}
                        </span>
                      </div>
                    </div>
                    <Button 
                      variant="outline" 
                      size="sm" 
                      onClick={() => {
                        const state = {
                          selectedOfferIds: pack.offers.map(o => o.offer.id),
                          userBudget: parseFloat(total_budget!),
                          ceremonyTypeId: parseInt(ceremony_type_id!),
                          city: city!,
                          eventDate: event_date!,
                          guestCount: guest_count ? parseInt(guest_count) : undefined
                        };
                        navigate('/event-pack-builder', { state });
                      }}
                    >
                      Voir le détail
                    </Button>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                    {pack.offers.map((item, i) => (
                      <div key={i} className="bg-surface-alt rounded-xl p-4 border border-border">
                        <div className="flex items-center gap-3 mb-2">
                          <Avatar
                            src={item.prestataire.avatar_url ? `${API_URL}${item.prestataire.avatar_url}` : undefined}
                            initials={item.prestataire.business_name.charAt(0)}
                            size="sm"
                          />
                          <div>
                            <p className="font-semibold text-text-primary truncate">
                              {item.prestataire.business_name}
                            </p>
                            <span className="text-xs text-primary-500 bg-primary-50 px-2 py-0.5 rounded-full">
                              {item.category_name}
                            </span>
                          </div>
                        </div>
                        <h4 className="font-medium text-text-primary mb-1 line-clamp-2">{item.offer.title}</h4>
                        <p className="text-xs text-text-secondary mb-2 line-clamp-2">{item.offer.description}</p>
                        <div className="flex justify-between items-center text-sm">
                          <span className="text-primary-500 font-bold">{formatPrice(item.offer.base_price || 0)}</span>
                          <span className="text-text-tertiary text-xs">Score: {item.individual_score.toFixed(2)}</span>
                        </div>
                      </div>
                    ))}
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