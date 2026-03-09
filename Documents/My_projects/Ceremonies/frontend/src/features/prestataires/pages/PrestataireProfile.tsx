// src/features/prestataires/pages/PrestataireProfile.tsx
import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  StarIcon as StarOutline,
  MapPinIcon,
  CalendarIcon,
  CurrencyEuroIcon,
  CheckBadgeIcon,
  ChatBubbleLeftRightIcon,
  HeartIcon as HeartOutline,
  ShareIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  XMarkIcon,
  PhoneIcon,
  EnvelopeIcon,
} from "@heroicons/react/24/outline";
import { HeartIcon as HeartSolid } from "@heroicons/react/24/solid";
import { StarIcon as StarSolid } from "@heroicons/react/24/solid";
import { Container } from "../../../shared/components/ui/Container";
import { Button } from "../../../shared/components/ui/Button";
import { Avatar } from "../../../shared/components/ui/Avatar";
import { Badge } from "../../../shared/components/ui/Badge";
import { useAuth } from "../../auth/hooks/useAuth";
import { prestatairesApi } from "../../../shared/api/prestataires";
import { serviceCategoriesApi } from "../../../shared/api/serviceCategories";
import { ceremonyTypesApi } from "../../../shared/api/ceremonyTypes";
import { prestataireFavoritesApi } from "../../../shared/api/prestataireFavorites";
import type { Prestataire, Offer, Review } from "../../../shared/api/prestataires";

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Composant Gallery
const Gallery = ({ mainImage }: { mainImage?: string | null }) => {
  if (!mainImage) {
    return (
      <div className="bg-gray-200 rounded-2xl h-64 flex items-center justify-center text-text-secondary">
        Aucune image
      </div>
    );
  }
  return (
    <div className="rounded-2xl overflow-hidden h-64">
      <img src={`${API_URL}${mainImage}`} alt="Image principale" className="w-full h-full object-cover" />
    </div>
  );
};

// Composant ReviewCard
const ReviewCard = ({ review }: { review: Review }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      className="bg-white rounded-xl p-6 shadow-soft border border-border"
    >
      <div className="flex items-start gap-4 mb-4">
        <Avatar src={review.avatar} alt={review.author || "Auteur"} size="md" />
        <div className="flex-1">
          <div className="flex justify-between items-start">
            <div>
              <h4 className="font-semibold text-text-primary">{review.author || "Client"}</h4>
              {review.eventType && <p className="text-xs text-text-tertiary">{review.eventType}</p>}
            </div>
            <div className="flex items-center gap-1">
              {[...Array(5)].map((_, i) => (
                <StarSolid
                  key={i}
                  className={`w-4 h-4 ${i < review.rating ? "text-gold-500" : "text-gray-200"}`}
                />
              ))}
            </div>
          </div>
          <p className="text-xs text-text-tertiary mt-1">
            {new Date(review.created_at).toLocaleDateString()}
          </p>
        </div>
      </div>
      <p className="text-text-secondary text-sm">{review.comment}</p>
    </motion.div>
  );
};

// Composant OfferCard avec badge du type de cérémonie
const OfferCard = ({ offer, ceremonyName }: { offer: Offer; ceremonyName?: string }) => {
  const navigate = useNavigate();
  return (
    <motion.div
      whileHover={{ y: -4 }}
      className="bg-white rounded-2xl p-6 border border-border shadow-soft relative"
    >
      <h3 className="text-xl font-bold text-text-primary mb-2">{offer.title}</h3>
      {ceremonyName && (
        <span className="inline-block bg-primary-50 text-primary-700 text-xs font-medium px-2 py-1 rounded-full mb-2">
          {ceremonyName}
        </span>
      )}
      <div className="flex items-end gap-1 mb-6">
        <span className="text-3xl font-bold text-primary-500">
          {offer.base_price ? `${offer.base_price}€` : "Sur devis"}
        </span>
      </div>
      <Button variant="outline" fullWidth onClick={() => navigate(`/offers/${offer.id}`)}>
        Voir l'offre
      </Button>
    </motion.div>
  );
};

export default function PrestataireProfile() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [prestataire, setPrestataire] = useState<Prestataire | null>(null);
  const [offers, setOffers] = useState<Offer[]>([]);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [categoryName, setCategoryName] = useState<string | null>(null);
  const [ceremonyTypesMap, setCeremonyTypesMap] = useState<Record<number, string>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"prestations" | "avis" | "infos">("prestations");
  const [isFavorite, setIsFavorite] = useState(false);
  const [favoriteLoading, setFavoriteLoading] = useState(false);

  useEffect(() => {
    if (!id) {
      setError("ID du prestataire manquant");
      setLoading(false);
      return;
    }
    const prestataireId = parseInt(id);
    if (isNaN(prestataireId)) {
      setError("ID du prestataire invalide");
      setLoading(false);
      return;
    }

    const fetchData = async () => {
      try {
        const [prestataireRes, offersRes, reviewsRes, ceremonyTypesRes] = await Promise.all([
          prestatairesApi.getPrestataire(prestataireId),
          prestatairesApi.getOffers(prestataireId),
          prestatairesApi.getReviews(prestataireId),
          ceremonyTypesApi.getAll(),
        ]);
        setPrestataire(prestataireRes.data);
        setOffers(offersRes.data);
        setReviews(reviewsRes.data);

        const map: Record<number, string> = {};
        ceremonyTypesRes.data.forEach(t => { map[t.id] = t.name; });
        setCeremonyTypesMap(map);

        if (prestataireRes.data.category_id) {
          const catRes = await serviceCategoriesApi.getOne(prestataireRes.data.category_id);
          setCategoryName(catRes.data.name);
        }

        // Vérifier si le prestataire est en favori (uniquement si l'utilisateur est connecté)
        if (user) {
          try {
            const favRes = await prestataireFavoritesApi.check(prestataireId);
            setIsFavorite(favRes.data.isFavorite);
          } catch (favErr) {
            console.error("Erreur vérification favori", favErr);
          }
        }
      } catch (error) {
        console.error("Erreur chargement profil prestataire", error);
        setError("Impossible de charger le profil du prestataire.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id, user]);

  const handleFavoriteToggle = async () => {
    if (!user) {
      navigate('/login');
      return;
    }
    if (!prestataire) return;
    setFavoriteLoading(true);
    try {
      if (isFavorite) {
        await prestataireFavoritesApi.remove(prestataire.id);
      } else {
        await prestataireFavoritesApi.add(prestataire.id);
      }
      setIsFavorite(!isFavorite);
    } catch (error) {
      console.error("Erreur lors du changement de favori", error);
      alert("Impossible de modifier les favoris. Veuillez réessayer.");
    } finally {
      setFavoriteLoading(false);
    }
  };

  const handleContact = (type: 'message' | 'whatsapp' | 'email') => {
    if (!prestataire) return;
    if (type === 'message') {
      navigate(`/messages?prestataire=${prestataire.id}`);
    } else if (type === 'whatsapp' && prestataire.whatsapp) {
      window.open(`https://wa.me/${prestataire.whatsapp.replace(/\s+/g, '')}`, '_blank');
    } else if (type === 'email') {
      alert("Email non disponible pour le moment");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background pt-24 flex justify-center">
        <div className="w-12 h-12 border-4 border-primary-200 border-t-primary-500 rounded-full animate-spin" />
      </div>
    );
  }

  if (error || !prestataire) {
    return (
      <div className="min-h-screen bg-background pt-24 text-center">
        <p className="text-text-secondary">{error || "Prestataire introuvable."}</p>
      </div>
    );
  }

  const averageRating =
    reviews.length > 0
      ? (reviews.reduce((acc, r) => acc + r.rating, 0) / reviews.length).toFixed(1)
      : "0.0";

  return (
    <div className="min-h-screen bg-background pt-24 pb-16">
      <Container>
        {/* En-tête */}
        <div className="mb-8">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-4">
            <div className="flex items-center gap-4">
              <Avatar
                size="lg"
                src={prestataire.avatar_url ? `${API_URL}${prestataire.avatar_url}` : undefined}
                initials={prestataire.business_name.charAt(0)}
              />
              <div>
                <div className="flex items-center gap-3 flex-wrap">
                  <h1 className="text-3xl md:text-4xl font-bold text-text-primary">
                    {prestataire.business_name}
                  </h1>
                  {prestataire.verified && <Badge variant="verified">Vérifié</Badge>}
                </div>
                {categoryName && <p className="text-text-secondary mt-1">{categoryName}</p>}
              </div>
            </div>
            <div className="flex gap-3">
              <Button
                variant="outline"
                size="sm"
                onClick={handleFavoriteToggle}
                disabled={favoriteLoading}
                className="flex items-center gap-2"
              >
                {isFavorite ? (
                  <HeartSolid className="w-5 h-5 text-red-500" />
                ) : (
                  <HeartOutline className="w-5 h-5 text-text-secondary" />
                )}
                <span className="hidden sm:inline">{isFavorite ? "Favori" : "Ajouter aux favoris"}</span>
              </Button>
              <Button variant="outline" size="sm" className="flex items-center gap-2">
                <ShareIcon className="w-5 h-5" />
                <span className="hidden sm:inline">Partager</span>
              </Button>
            </div>
          </div>

          {/* Tags et métriques */}
          <div className="flex flex-wrap gap-6 text-sm">
            <div className="flex items-center gap-2">
              <MapPinIcon className="w-5 h-5 text-text-tertiary" />
              <span className="text-text-secondary">{prestataire.city || "Localisation non renseignée"}</span>
            </div>
            <div className="flex items-center gap-2">
              <StarOutline className="w-5 h-5 text-gold-500" />
              <span className="font-semibold text-text-primary">{averageRating}</span>
              <span className="text-text-tertiary">({reviews.length} avis)</span>
            </div>
            <div className="flex items-center gap-2">
              <CalendarIcon className="w-5 h-5 text-text-tertiary" />
              <span className="text-text-secondary">
                Membre depuis {new Date(prestataire.created_at).getFullYear()}
              </span>
            </div>
          </div>
        </div>

        {/* Grille principale */}
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Colonne de gauche */}
          <div className="lg:col-span-2 space-y-8">
            <Gallery mainImage={prestataire.business_image_url} />
            <div className="bg-white rounded-2xl p-6 shadow-soft">
              <h2 className="text-xl font-bold text-text-primary mb-4">À propos</h2>
              <p className="text-text-secondary whitespace-pre-line">
                {prestataire.description || "Aucune description fournie."}
              </p>
            </div>

            {/* Tabs */}
            <div className="bg-white rounded-2xl shadow-soft overflow-hidden">
              <div className="flex border-b border-border">
                {["prestations", "avis", "infos"].map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab as any)}
                    className={`flex-1 py-4 text-sm font-medium transition-colors relative ${
                      activeTab === tab ? "text-primary-500" : "text-text-secondary hover:text-text-primary"
                    }`}
                  >
                    {tab === "prestations" && "Prestations"}
                    {tab === "avis" && `Avis (${reviews.length})`}
                    {tab === "infos" && "Informations"}
                    {activeTab === tab && (
                      <motion.div
                        layoutId="activeTab"
                        className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary-500"
                      />
                    )}
                  </button>
                ))}
              </div>

              <div className="p-6">
                <AnimatePresence mode="wait">
                  {activeTab === "prestations" && (
                    <motion.div
                      key="prestations"
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      className="space-y-4"
                    >
                      {offers.length === 0 ? (
                        <p className="text-text-secondary">Aucune offre pour le moment.</p>
                      ) : (
                        offers.map((offer) => (
                          <OfferCard
                            key={offer.id}
                            offer={offer}
                            ceremonyName={ceremonyTypesMap[offer.ceremony_type_id]}
                          />
                        ))
                      )}
                    </motion.div>
                  )}

                  {activeTab === "avis" && (
                    <motion.div
                      key="avis"
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      className="space-y-4"
                    >
                      {reviews.length === 0 ? (
                        <p className="text-text-secondary">Aucun avis pour le moment.</p>
                      ) : (
                        reviews.map((review) => <ReviewCard key={review.id} review={review} />)
                      )}
                    </motion.div>
                  )}

                  {activeTab === "infos" && (
                    <motion.div
                      key="infos"
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      className="space-y-4"
                    >
                      <div className="flex items-center gap-4 py-3 border-b border-border">
                        <MapPinIcon className="w-5 h-5 text-text-tertiary" />
                        <span className="text-text-secondary">{prestataire.city || "Non renseignée"}</span>
                      </div>
                      <div className="flex items-center gap-4 py-3 border-b border-border">
                        <CalendarIcon className="w-5 h-5 text-text-tertiary" />
                        <span className="text-text-secondary">Disponible sur demande</span>
                      </div>
                      <div className="flex items-center gap-4 py-3">
                        <CurrencyEuroIcon className="w-5 h-5 text-text-tertiary" />
                        <span className="text-text-secondary">Paiement en ligne sécurisé</span>
                      </div>
                      {prestataire.map_url && (
                        <div className="py-3">
                          <a href={prestataire.map_url} target="_blank" rel="noopener noreferrer" className="text-primary-500 hover:underline">
                            Voir sur Google Maps
                          </a>
                        </div>
                      )}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </div>
          </div>

          {/* Colonne de droite */}
          <div className="space-y-6">
            {/* Carte de contact */}
            <div className="bg-white rounded-2xl p-6 shadow-soft sticky top-24">
              <h2 className="text-xl font-bold text-text-primary mb-4">Contacter</h2>
              <div className="space-y-4 mb-6">
                <Button
                  variant="primary"
                  fullWidth
                  className="flex items-center justify-center gap-2"
                  onClick={() => handleContact('message')}
                >
                  <ChatBubbleLeftRightIcon className="w-5 h-5" />
                  Envoyer un message
                </Button>
                {prestataire.whatsapp ? (
                  <Button
                    variant="outline"
                    fullWidth
                    className="flex items-center justify-center gap-2"
                    onClick={() => handleContact('whatsapp')}
                  >
                    <PhoneIcon className="w-5 h-5" />
                    WhatsApp
                  </Button>
                ) : (
                  <Button variant="outline" fullWidth disabled className="flex items-center justify-center gap-2">
                    <PhoneIcon className="w-5 h-5" />
                    WhatsApp non renseigné
                  </Button>
                )}
                <Button
                  variant="outline"
                  fullWidth
                  className="flex items-center justify-center gap-2"
                  onClick={() => handleContact('email')}
                >
                  <EnvelopeIcon className="w-5 h-5" />
                  Contacter par email
                </Button>
              </div>
              <div className="border-t border-border pt-4">
                <p className="text-xs text-text-tertiary text-center">
                  En nous contactant, vous acceptez nos conditions d'utilisation.
                </p>
              </div>
            </div>

            {/* Badge de confiance */}
            <div className="bg-gradient-to-br from-primary-50 to-gold-50 rounded-2xl p-6 text-center">
              <CheckBadgeIcon className="w-12 h-12 text-primary-500 mx-auto mb-3" />
              <h3 className="font-semibold text-text-primary mb-2">
                {prestataire.verified ? "Prestataire vérifié" : "En attente de vérification"}
              </h3>
              <p className="text-xs text-text-secondary">
                {prestataire.verified
                  ? "Son identité et ses documents ont été vérifiés."
                  : "Ce prestataire est en cours de vérification."}
              </p>
            </div>
          </div>
        </div>
      </Container>
    </div>
  );
}