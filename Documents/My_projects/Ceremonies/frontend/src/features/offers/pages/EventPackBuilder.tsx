import { useState, useEffect, useMemo } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  CurrencyEuroIcon,
  UserIcon,
  StarIcon,
  MapPinIcon,
  ShieldCheckIcon,
  SparklesIcon,
  CheckCircleIcon,
  PlusIcon,
  TrashIcon,
} from "@heroicons/react/24/outline";
import { StarIcon as StarIconSolid } from "@heroicons/react/24/solid";
import { Container } from "../../../shared/components/ui/Container";
import { Card } from "../../../shared/components/ui/Card";
import { Button } from "../../../shared/components/ui/Button";
import { Avatar } from "../../../shared/components/ui/Avatar";
import { Modal } from "../../../shared/components/ui/Modal";
import { Input } from "../../../shared/components/ui/Input";
import { offersApi } from "../../../shared/api/offers";
import { prestatairesApi } from "../../../shared/api/prestataires";
import { ceremonyTypesApi } from "../../../shared/api/ceremonyTypes";
import { serviceCategoriesApi } from "../../../shared/api/serviceCategories";
import { packsApi } from "../../../shared/api/packs";
import { useEventCompletionScore } from "../hooks/useEventCompletionScore";
import type { Offer } from "../../../shared/api/offers";
import type { Prestataire } from "../../../shared/api/prestataires";

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Composant pour la carte d'offre dans le pack
function PackOfferCard({
  offer,
  prestataire,
  categoryName,
  onReplace,
  onRemove,
  onViewOffer,
  onViewPrestataire,
}: {
  offer: Offer;
  prestataire: Prestataire;
  categoryName: string;
  onReplace: () => void;
  onRemove: () => void;
  onViewOffer: () => void;
  onViewPrestataire: () => void;
}) {
  return (
    <Card className="p-4 hover:shadow-medium transition-all duration-300 relative">
      <div className="flex items-start gap-3">
        <Avatar
          src={prestataire.avatar_url ? `${API_URL}${prestataire.avatar_url}` : undefined}
          initials={prestataire.business_name.charAt(0)}
          size="sm"
        />
        <div className="flex-1">
          <div className="flex justify-between">
            <div>
              <h4 className="font-semibold text-text-primary">{offer.title}</h4>
              <p className="text-xs text-text-secondary line-clamp-2">{offer.description}</p>
            </div>
            <span className="text-primary-500 font-bold">{offer.base_price}€</span>
          </div>
          <div className="flex items-center gap-2 mt-2 text-xs">
            <span className="bg-primary-50 text-primary-700 px-2 py-0.5 rounded-full">
              {categoryName}
            </span>
            {prestataire.verified && (
              <ShieldCheckIcon className="w-4 h-4 text-green-600" title="Vérifié" />
            )}
          </div>
          <div className="flex items-center gap-2 mt-3">
            <button onClick={onViewOffer} className="text-xs text-primary-500 hover:underline">
              Voir l'offre
            </button>
            <span className="text-text-tertiary">•</span>
            <button onClick={onViewPrestataire} className="text-xs text-primary-500 hover:underline">
              Voir le prestataire
            </button>
            <span className="text-text-tertiary">•</span>
            <button onClick={onReplace} className="text-xs text-primary-500 hover:underline">
              Remplacer
            </button>
            <button onClick={onRemove} className="text-xs text-red-500 hover:underline ml-auto">
              <TrashIcon className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </Card>
  );
}

// Composant pour la modal de remplacement (appel API réel)
function ReplaceOfferModal({
  isOpen,
  onClose,
  categoryId,
  city,
  onSelect,
}: {
  isOpen: boolean;
  onClose: () => void;
  categoryId: number;
  city: string;
  onSelect: (newOfferId: number) => void;
}) {
  const [offers, setOffers] = useState<Offer[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setLoading(true);
      // Appel API pour récupérer les offres de la catégorie donnée dans la même ville
      // À adapter selon votre endpoint réel (ex: /offers?category_id=...&city=...)
      offersApi.getAll().then(res => {
        // Filtrer côté client (à remplacer par un appel filtré si possible)
        const filtered = res.data.filter(o => {
          // Ici on aurait besoin de la catégorie du prestataire, on simplifie
          return true;
        });
        setOffers(filtered);
        setLoading(false);
      }).catch(() => setLoading(false));
    }
  }, [isOpen, categoryId, city]);

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Choisir une offre">
      <div className="space-y-4 max-h-96 overflow-y-auto">
        {loading ? (
          <p>Chargement...</p>
        ) : (
          offers.map(offer => (
            <Card key={offer.id} className="p-4 cursor-pointer hover:bg-surface-alt" onClick={() => onSelect(offer.id)}>
              <div className="flex justify-between">
                <div>
                  <h4 className="font-semibold">{offer.title}</h4>
                  <p className="text-sm text-text-secondary">{offer.description}</p>
                </div>
                <span className="text-primary-500 font-bold">{offer.base_price}€</span>
              </div>
            </Card>
          ))
        )}
      </div>
    </Modal>
  );
}

export default function EventPackBuilder() {
  const location = useLocation();
  const navigate = useNavigate();
  const { packId } = useParams<{ packId: string }>(); // optionnel : si on édite un pack existant
  const state = location.state as any;

  // Données de base
  const [offers, setOffers] = useState<Offer[]>([]);
  const [prestatairesMap, setPrestatairesMap] = useState<Record<number, Prestataire>>({});
  const [categoryNameMap, setCategoryNameMap] = useState<Record<number, string>>({});
  const [categoryIdMap, setCategoryIdMap] = useState<Record<string, number>>({}); // nom -> id
  const [ceremonyTypesMap, setCeremonyTypesMap] = useState<Record<number, any>>({});
  const [loading, setLoading] = useState(true);
  const [dataLoaded, setDataLoaded] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [scoreLoading, setScoreLoading] = useState(true); // Nouvel état pour le score

  // État du pack
  const [packName, setPackName] = useState('');
  const [selectedOfferIds, setSelectedOfferIds] = useState<Set<number>>(new Set());
  const [userBudget, setUserBudget] = useState<number | null>(null);
  const [ceremonyTypeId, setCeremonyTypeId] = useState<number | null>(null);
  const [city, setCity] = useState('');
  const [eventDate, setEventDate] = useState('');

  // Modal de remplacement
  const [replaceModalOpen, setReplaceModalOpen] = useState(false);
  const [replaceCategoryId, setReplaceCategoryId] = useState<number | null>(null);
  const [replaceOfferId, setReplaceOfferId] = useState<number | null>(null);

  // Charger les données de base (offres, prestataires, catégories)
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [offersRes, ceremonyTypesRes, categoriesRes] = await Promise.all([
          offersApi.getAll(),
          ceremonyTypesApi.getAll(),
          serviceCategoriesApi.getAll(),
        ]);
        setOffers(offersRes.data);
        console.log('Offres chargées:', offersRes.data.length);

        const ceremonyMap: Record<number, any> = {};
        ceremonyTypesRes.data.forEach(ct => {
          ceremonyMap[ct.id] = ct;
        });
        setCeremonyTypesMap(ceremonyMap);

        const catMap: Record<number, string> = {};
        const catIdMap: Record<string, number> = {};
        categoriesRes.data.forEach(cat => {
          catMap[cat.id] = cat.name;
          catIdMap[cat.name] = cat.id;
        });
        setCategoryNameMap(catMap);
        setCategoryIdMap(catIdMap);
        console.log('Catégories chargées:', categoriesRes.data.length);

        // Récupérer les prestataires uniques
        const prestataireIds = Array.from(new Set(offersRes.data.map(o => o.prestataire_id)));
        console.log('IDs prestataires uniques:', prestataireIds.length);
        const prestatairePromises = prestataireIds.map(id => prestatairesApi.getPrestataire(id));
        const prestataireResponses = await Promise.all(prestatairePromises);
        const prestaMap: Record<number, Prestataire> = {};
        prestataireResponses.forEach(res => {
          prestaMap[res.data.id] = res.data;
        });
        setPrestatairesMap(prestaMap);
        console.log('Prestataires chargés:', Object.keys(prestaMap).length);

        setDataLoaded(true);
      } catch (err) {
        console.error("Erreur chargement des données", err);
        setError("Impossible de charger les données.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  // Charger un pack existant si packId est présent
  useEffect(() => {
    if (packId) {
      const fetchPack = async () => {
        try {
          const res = await packsApi.getOne(parseInt(packId));
          const pack = res.data;
          setPackName(pack.name);
          setSelectedOfferIds(new Set(pack.offers.map(o => o.offer_id)));
          setUserBudget(pack.user_budget ?? null);
          // Les autres infos (city, eventDate, ceremonyTypeId) ne sont pas stockées dans le pack – à récupérer ailleurs si besoin
        } catch (err) {
          console.error("Erreur chargement pack", err);
          setError("Impossible de charger le pack.");
        }
      };
      fetchPack();
    } else if (state) {
      // Initialisation depuis l'état (création)
      setSelectedOfferIds(new Set(state.selectedOfferIds || []));
      setUserBudget(state.userBudget || null);
      setCeremonyTypeId(state.ceremonyTypeId || null);
      setCity(state.city || '');
      setEventDate(state.eventDate || '');
      setPackName(state.packName || 'Mon pack');
      console.log('État initial reçu:', state);
    }
  }, [packId, state]);

  // Liste des offres sélectionnées
  const selectedOffers = useMemo(() => {
    return Array.from(selectedOfferIds).map(id => offers.find(o => o.id === id)).filter(Boolean) as Offer[];
  }, [selectedOfferIds, offers]);

  // Calcul du budget total
  const totalPrice = useMemo(() => {
    return selectedOffers.reduce((sum, o) => sum + (o.base_price || 0), 0);
  }, [selectedOffers]);

  // Pourcentage d'utilisation du budget
  const budgetPercent = useMemo(() => {
    return userBudget ? Math.min(100, (totalPrice / userBudget) * 100) : 0;
  }, [totalPrice, userBudget]);

  // Catégories disponibles pour ce type de cérémonie (si ceremonyTypeId est fourni)
  const availableCategories = useMemo(() => {
    if (!ceremonyTypeId) return [];
    const filtered = offers.filter(o => o.ceremony_type_id === ceremonyTypeId);
    const categories = new Set<string>();
    filtered.forEach(offer => {
      const prestataire = prestatairesMap[offer.prestataire_id];
      if (prestataire?.category_id) {
        const catName = categoryNameMap[prestataire.category_id];
        if (catName) categories.add(catName);
      }
    });
    const result = Array.from(categories);
    console.log('availableCategories', result, 'pour ceremonyTypeId', ceremonyTypeId);
    return result;
  }, [offers, ceremonyTypeId, prestatairesMap, categoryNameMap]);

  // Catégories couvertes par les offres sélectionnées
  const coveredCategories = useMemo(() => {
    const covered = new Set<string>();
    selectedOffers.forEach(offer => {
      const prestataire = prestatairesMap[offer.prestataire_id];
      if (prestataire?.category_id) {
        const catName = categoryNameMap[prestataire.category_id];
        if (catName) covered.add(catName);
      }
    });
    console.log('coveredCategories', Array.from(covered));
    return covered;
  }, [selectedOffers, prestatairesMap, categoryNameMap]);

  // Catégories manquantes
  const missingCategories = useMemo(() => {
    return availableCategories.filter(cat => !coveredCategories.has(cat));
  }, [availableCategories, coveredCategories]);

  // Score de complétude local (pour l'affichage en temps réel)
  const localCompletionScore = useEventCompletionScore({
    selectedOfferIds,
    offers,
    prestatairesMap,
    categoryNameMap,
    importantCategories: availableCategories,
    userBudget: userBudget, // peut être null, le hook gère
  });

  // Gérer le chargement du score
  useEffect(() => {
    if (localCompletionScore !== null) {
      setScoreLoading(false);
    } else {
      setScoreLoading(true);
    }
  }, [localCompletionScore]);

  // Log du score
  useEffect(() => {
    console.log('localCompletionScore', localCompletionScore);
  }, [localCompletionScore]);

  // Sauvegarder le pack
  const handleSave = async () => {
    setSaving(true);
    try {
      if (packId) {
        // Mise à jour
        await packsApi.update(parseInt(packId), {
          name: packName,
          offer_ids: Array.from(selectedOfferIds),
          user_budget: userBudget,
        });
      } else {
        // Création
        await packsApi.create({
          name: packName,
          event_id: null,
          user_budget: userBudget,
          offer_ids: Array.from(selectedOfferIds),
        });
      }
      navigate('/marketplace'); // ou vers une page de liste des packs
    } catch (err) {
      console.error("Erreur sauvegarde pack", err);
      alert("Erreur lors de la sauvegarde.");
    } finally {
      setSaving(false);
    }
  };

  // Gestion suppression
  const handleRemove = (offerId: number) => {
    setSelectedOfferIds(prev => {
      const newSet = new Set(prev);
      newSet.delete(offerId);
      return newSet;
    });
  };

  // Gestion remplacement
  const handleReplace = (offerId: number, categoryName: string) => {
    const catId = categoryIdMap[categoryName];
    if (catId) {
      setReplaceOfferId(offerId);
      setReplaceCategoryId(catId);
      setReplaceModalOpen(true);
    }
  };

  // Sélection d'une nouvelle offre
  const handleSelectReplace = (newOfferId: number) => {
    if (replaceOfferId) {
      setSelectedOfferIds(prev => {
        const newSet = new Set(prev);
        newSet.delete(replaceOfferId);
        newSet.add(newOfferId);
        return newSet;
      });
    }
    setReplaceModalOpen(false);
    setReplaceOfferId(null);
  };

  // Gestion ajout catégorie manquante
  const handleAddCategory = (categoryName: string) => {
    const catId = categoryIdMap[categoryName];
    if (catId) {
      setReplaceCategoryId(catId);
      setReplaceOfferId(null);
      setReplaceModalOpen(true);
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
        <Button variant="primary" onClick={() => navigate(-1)} className="mt-4">
          Retour
        </Button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background pt-24 pb-16">
      <Container>
        <div className="flex items-center gap-2 text-text-secondary mb-6">
          <button onClick={() => navigate(-1)} className="hover:text-primary-500">
            ← Retour
          </button>
        </div>

        <div className="flex justify-between items-center mb-6">
          <Input
            value={packName}
            onChange={(e) => setPackName(e.target.value)}
            placeholder="Nom du pack"
            className="text-2xl font-bold w-96"
          />
          <Button variant="primary" onClick={handleSave} disabled={saving}>
            {saving ? "Sauvegarde..." : "Sauvegarder le pack"}
          </Button>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Colonne principale */}
          <div className="lg:col-span-2 space-y-6">
            {/* Récapitulatif budget */}
            <Card className="p-6">
              <div className="flex flex-wrap gap-6">
                <div>
                  <p className="text-sm text-text-secondary">Budget total</p>
                  <p className="text-2xl font-bold text-primary-500">{totalPrice.toFixed(0)}€</p>
                </div>
                <div>
                  <p className="text-sm text-text-secondary">Budget utilisateur</p>
                  <Input
                    type="number"
                    value={userBudget || ''}
                    onChange={(e) => setUserBudget(e.target.value ? parseFloat(e.target.value) : null)}
                    placeholder="Budget"
                    className="w-32"
                  />
                </div>
                <div>
                  <p className="text-sm text-text-secondary">Utilisation</p>
                  <p className="text-2xl font-bold text-text-primary">{budgetPercent.toFixed(0)}%</p>
                </div>
              </div>
              <div className="mt-4 w-full bg-gray-200 rounded-full h-2.5">
                <div
                  className="bg-primary-500 h-2.5 rounded-full transition-all duration-300"
                  style={{ width: `${budgetPercent}%` }}
                ></div>
              </div>
            </Card>

            {/* Score local - affiché uniquement si un type de cérémonie a été sélectionné */}
            {dataLoaded && ceremonyTypeId && (
              scoreLoading ? (
                <Card className="p-6">
                  <p className="text-text-secondary">Calcul du score en cours...</p>
                </Card>
              ) : localCompletionScore && (
                <Card className="p-6">
                  <h2 className="text-xl font-bold text-text-primary mb-4">Score estimé</h2>
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-4 text-sm">
                    <div>
                      <p className="text-text-secondary">Global</p>
                      <p className="text-2xl font-bold text-primary-500">{localCompletionScore.total}/100</p>
                    </div>
                    <div>
                      <p className="text-text-secondary">Catégories</p>
                      <p className="text-lg font-bold">{localCompletionScore.categoryCoverage.toFixed(0)}%</p>
                    </div>
                    <div>
                      <p className="text-text-secondary">Qualité</p>
                      <p className="text-lg font-bold">{localCompletionScore.quality.toFixed(0)}%</p>
                    </div>
                    <div>
                      <p className="text-text-secondary">Budget</p>
                      <p className="text-lg font-bold">{localCompletionScore.budgetFit.toFixed(0)}%</p>
                    </div>
                    <div>
                      <p className="text-text-secondary">Interaction</p>
                      <p className="text-lg font-bold">{localCompletionScore.userInteraction.toFixed(0)}%</p>
                    </div>
                  </div>
                </Card>
              )
            )}

            {/* Liste des offres */}
            <div className="space-y-4">
              <h2 className="text-xl font-bold text-text-primary">Vos prestations ({selectedOffers.length})</h2>
              {selectedOffers.map(offer => {
                const prestataire = prestatairesMap[offer.prestataire_id];
                if (!prestataire) return null;
                const categoryName = categoryNameMap[prestataire.category_id || 0] || 'Inconnue';
                return (
                  <PackOfferCard
                    key={offer.id}
                    offer={offer}
                    prestataire={prestataire}
                    categoryName={categoryName}
                    onReplace={() => handleReplace(offer.id, categoryName)}
                    onRemove={() => handleRemove(offer.id)}
                    onViewOffer={() => navigate(`/offers/${offer.id}`)}
                    onViewPrestataire={() => navigate(`/prestataire/${prestataire.id}`)}
                  />
                );
              })}
            </div>
          </div>

          {/* Colonne latérale */}
          <div className="space-y-6">
            {missingCategories.length > 0 && (
              <Card className="p-6">
                <h3 className="font-bold text-text-primary mb-4">Catégories manquantes</h3>
                <div className="space-y-3">
                  {missingCategories.map(cat => (
                    <div key={cat} className="flex justify-between items-center">
                      <span className="text-sm text-text-secondary">{cat}</span>
                      <Button variant="outline" size="sm" onClick={() => handleAddCategory(cat)}>
                        <PlusIcon className="w-4 h-4 mr-1" />
                        Ajouter
                      </Button>
                    </div>
                  ))}
                </div>
              </Card>
            )}

            {/* Suggestions simples */}
            {totalPrice > (userBudget || 0) && (
              <Card className="p-6 bg-primary-50">
                <h3 className="font-bold text-text-primary mb-4 flex items-center gap-2">
                  <SparklesIcon className="w-5 h-5 text-gold-500" />
                  Suggestion
                </h3>
                <p className="text-sm text-text-secondary">
                  Votre budget est dépassé de {(totalPrice - (userBudget || 0)).toFixed(0)}€.
                </p>
              </Card>
            )}
          </div>
        </div>
      </Container>

      {/* Modal de remplacement */}
      {replaceCategoryId && (
        <ReplaceOfferModal
          isOpen={replaceModalOpen}
          onClose={() => setReplaceModalOpen(false)}
          categoryId={replaceCategoryId}
          city={city}
          onSelect={handleSelectReplace}
        />
      )}
    </div>
  );
}