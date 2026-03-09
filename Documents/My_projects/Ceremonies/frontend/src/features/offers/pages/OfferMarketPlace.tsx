import { useState, useEffect, useMemo } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  CurrencyEuroIcon,
  UserIcon,
  CalendarIcon,
  StarIcon,
  SparklesIcon,
  PlusIcon,
  CheckIcon,
  XMarkIcon,
} from "@heroicons/react/24/outline";
import { Container } from "../../../shared/components/ui/Container";
import { Card } from "../../../shared/components/ui/Card";
import { Button } from "../../../shared/components/ui/Button";
import { offersApi } from "../../../shared/api/offers";
import { prestatairesApi } from "../../../shared/api/prestataires";
import { ceremonyTypesApi } from "../../../shared/api/ceremonyTypes";
import { serviceCategoriesApi } from "../../../shared/api/serviceCategories";
import type { Offer } from "../../../shared/api/offers";
import type { Prestataire } from "../../../shared/api/prestataires";
import type { CeremonyType } from "../../../shared/api/ceremonyTypes";
import type { ServiceCategory } from "../../../shared/api/serviceCategories";
import { useEventCompletionScore } from "../hooks/useEventCompletionScore";

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function OfferMarketplace() {
  const navigate = useNavigate();
  const [offers, setOffers] = useState<Offer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [prestatairesMap, setPrestatairesMap] = useState<Record<number, Prestataire>>({});
  const [ceremonyTypesMap, setCeremonyTypesMap] = useState<Record<number, CeremonyType>>({});
  const [categoryNameMap, setCategoryNameMap] = useState<Record<number, string>>({});

  // Filtre par type de cérémonie
  const [selectedCeremonyTypeId, setSelectedCeremonyTypeId] = useState<number | null>(null);

  // Offres sélectionnées (pack manuel)
  const [selectedOfferIds, setSelectedOfferIds] = useState<Set<number>>(new Set());

  // Budget utilisateur pour l'affichage local du score (non transmis au pack)
  const LOCAL_BUDGET = 5000;

  // Récupération des données
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [offersRes, ceremonyTypesRes, categoriesRes] = await Promise.all([
          offersApi.getAll(),
          ceremonyTypesApi.getAll(),
          serviceCategoriesApi.getAll(),
        ]);
        setOffers(offersRes.data);

        const ceremonyMap: Record<number, CeremonyType> = {};
        ceremonyTypesRes.data.forEach(ct => {
          ceremonyMap[ct.id] = ct;
        });
        setCeremonyTypesMap(ceremonyMap);

        const catMap: Record<number, string> = {};
        categoriesRes.data.forEach(cat => {
          catMap[cat.id] = cat.name;
        });
        setCategoryNameMap(catMap);

        // Récupérer les prestataires uniques
        const prestataireIds = Array.from(new Set(offersRes.data.map(o => o.prestataire_id)));
        const prestatairePromises = prestataireIds.map(id => prestatairesApi.getPrestataire(id));
        const prestataireResponses = await Promise.all(prestatairePromises);
        const prestaMap: Record<number, Prestataire> = {};
        prestataireResponses.forEach(res => {
          prestaMap[res.data.id] = res.data;
        });
        setPrestatairesMap(prestaMap);

      } catch (err) {
        console.error("Erreur chargement des offres", err);
        setError("Impossible de charger les offres.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  // Filtrer les offres selon le type de cérémonie sélectionné
  const filteredOffers = selectedCeremonyTypeId
    ? offers.filter(o => o.ceremony_type_id === selectedCeremonyTypeId)
    : offers;

  // Calcul du budget total du pack
  const totalBudget = useMemo(() => {
    return Array.from(selectedOfferIds).reduce((sum, id) => {
      const offer = offers.find(o => o.id === id);
      return sum + (offer?.base_price || 0);
    }, 0);
  }, [selectedOfferIds, offers]);

  // --- DYNAMIQUE RÉELLE ---
  // 1. Catégories disponibles pour le type de cérémonie sélectionné
  const availableCategoriesForType = useMemo(() => {
    if (!selectedCeremonyTypeId) return [];
    const categoriesSet = new Set<string>();
    filteredOffers.forEach(offer => {
      const prestataire = prestatairesMap[offer.prestataire_id];
      if (prestataire?.category_id) {
        const catName = categoryNameMap[prestataire.category_id];
        if (catName) categoriesSet.add(catName);
      }
    });
    return Array.from(categoriesSet);
  }, [selectedCeremonyTypeId, filteredOffers, prestatairesMap, categoryNameMap]);

  // 2. Catégories déjà couvertes par les offres sélectionnées
  const coveredCategories = useMemo(() => {
    if (!selectedCeremonyTypeId) return new Set<string>();
    const covered = new Set<string>();
    selectedOfferIds.forEach(id => {
      const offer = offers.find(o => o.id === id);
      if (offer) {
        const prestataire = prestatairesMap[offer.prestataire_id];
        if (prestataire?.category_id) {
          const catName = categoryNameMap[prestataire.category_id];
          if (catName && availableCategoriesForType.includes(catName)) {
            covered.add(catName);
          }
        }
      }
    });
    return covered;
  }, [selectedCeremonyTypeId, selectedOfferIds, offers, prestatairesMap, categoryNameMap, availableCategoriesForType]);

  // 3. Catégories manquantes
  const missingCategories = useMemo(() => {
    if (!selectedCeremonyTypeId) return [];
    return availableCategoriesForType.filter(cat => !coveredCategories.has(cat));
  }, [selectedCeremonyTypeId, availableCategoriesForType, coveredCategories]);

  // 4. Score de complétude local (pour l'affichage seulement)
  const completionScore = useEventCompletionScore({
    selectedOfferIds,
    offers,
    prestatairesMap,
    categoryNameMap,
    importantCategories: availableCategoriesForType,
    userBudget: LOCAL_BUDGET, // utilisé uniquement pour l'affichage du score
  });

  // Gestion de la sélection
  const toggleOffer = (offerId: number) => {
    setSelectedOfferIds(prev => {
      const newSet = new Set(prev);
      if (newSet.has(offerId)) {
        newSet.delete(offerId);
      } else {
        newSet.add(offerId);
      }
      return newSet;
    });
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
        <Button variant="primary" onClick={() => navigate(0)} className="mt-4">
          Réessayer
        </Button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background pt-24 pb-16">
      <Container>
        {/* En-tête avec bouton de recommandations */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold text-text-primary mb-2">
              Construisez votre événement
            </h1>
            <p className="text-text-secondary text-lg">
              Sélectionnez des offres pour créer votre pack personnalisé
            </p>
          </div>
          <div className="flex flex-col items-end">
            <Button
              variant="primary"
              onClick={() => navigate("/event-builder")}
              className="relative overflow-hidden group text-lg px-8 py-4 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
            >
              <span className="relative z-10 flex items-center gap-2">
                <SparklesIcon className="w-5 h-5" />
                Profiter de nos suggestions intelligentes
              </span>
              <span className="absolute inset-0 bg-gradient-to-r from-primary-600 to-primary-400 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></span>
            </Button>
          </div>
        </div>

        {/* Filtre par type de cérémonie */}
        <div className="flex flex-wrap gap-4 mb-8">
          <div className="w-full md:w-auto">
            <label htmlFor="ceremony-filter" className="block text-sm font-medium text-text-primary mb-2">
              Filtrer par type de cérémonie
            </label>
            <select
              id="ceremony-filter"
              value={selectedCeremonyTypeId ?? ""}
              onChange={(e) => setSelectedCeremonyTypeId(e.target.value ? parseInt(e.target.value) : null)}
              className="w-full md:w-64 px-4 py-2 rounded-xl border border-border bg-white focus:outline-none focus:ring-2 focus:ring-primary-500/30"
            >
              <option value="">Tous</option>
              {Object.values(ceremonyTypesMap).map(type => (
                <option key={type.id} value={type.id}>{type.name}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Section de complétude locale (uniquement si type sélectionné) */}
        {selectedOfferIds.size > 0 && selectedCeremonyTypeId && completionScore && (
          <div className="mb-8 p-6 bg-white rounded-2xl shadow-soft border border-border">
            <h2 className="text-xl font-bold text-text-primary mb-4">Score estimé de votre événement</h2>
            
            {/* Score global */}
            <div className="mb-4">
              <div className="flex justify-between text-sm mb-1">
                <span className="text-text-secondary">Score global</span>
                <span className="font-medium text-primary-500">{completionScore.total}/100</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div
                  className="bg-primary-500 h-2.5 rounded-full transition-all duration-300"
                  style={{ width: `${completionScore.total}%` }}
                ></div>
              </div>
            </div>

            {/* Sous-scores */}
            <div className="grid grid-cols-2 gap-4 text-sm mt-3">
              <div>
                <span className="text-text-secondary">Catégories :</span>
                <span className="ml-2 font-medium">{completionScore.categoryCoverage.toFixed(0)}%</span>
              </div>
              <div>
                <span className="text-text-secondary">Interaction :</span>
                <span className="ml-2 font-medium">{completionScore.userInteraction.toFixed(0)}%</span>
              </div>
              <div>
                <span className="text-text-secondary">Qualité :</span>
                <span className="ml-2 font-medium">{completionScore.quality.toFixed(0)}%</span>
              </div>
              <div>
                <span className="text-text-secondary">Budget :</span>
                <span className="ml-2 font-medium">{completionScore.budgetFit.toFixed(0)}%</span>
              </div>
            </div>

            {/* Suggestions de catégories manquantes */}
            {missingCategories.length > 0 && (
              <div className="mt-4 pt-4 border-t border-border">
                <p className="text-sm text-text-secondary mb-2">Pour améliorer votre score, ajoutez :</p>
                <div className="flex flex-wrap gap-2">
                  {missingCategories.map(cat => (
                    <span key={cat} className="px-3 py-1 bg-primary-50 text-primary-700 rounded-full text-sm">
                      {cat}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Message informatif si offres sélectionnées sans type */}
        {selectedOfferIds.size > 0 && !selectedCeremonyTypeId && (
          <div className="mb-8 p-4 bg-amber-50 border border-amber-200 rounded-xl">
            <p className="text-sm text-amber-800">
              Veuillez sélectionner un type de cérémonie pour bénéficier de notre analyse intelligente de complétude.
            </p>
          </div>
        )}

        {/* Grille des offres */}
        {filteredOffers.length === 0 ? (
          <p className="text-text-secondary text-center py-12">
            Aucune offre disponible pour ce type de cérémonie.
          </p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredOffers.map((offer, index) => {
              const prestataire = prestatairesMap[offer.prestataire_id];
              const ceremonyType = ceremonyTypesMap[offer.ceremony_type_id];
              const isSelected = selectedOfferIds.has(offer.id);
              return (
                <motion.div
                  key={offer.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  whileHover={{ y: -5 }}
                  className="group"
                >
                  <Card className={`p-6 h-full flex flex-col hover:shadow-medium transition-all duration-300 ${isSelected ? 'ring-2 ring-primary-500' : ''}`}>
                    <div className="flex-1">
                      <h3 className="text-xl font-bold text-text-primary mb-2 line-clamp-2">
                        {offer.title}
                      </h3>
                      {ceremonyType && (
                        <span className="inline-block bg-primary-50 text-primary-700 text-xs font-medium px-2 py-1 rounded-full mb-3">
                          {ceremonyType.name}
                        </span>
                      )}
                      <p className="text-text-secondary text-sm mb-4 line-clamp-3">
                        {offer.description || "Aucune description"}
                      </p>
                      <div className="flex items-center gap-2 text-2xl font-bold text-primary-500 mb-4">
                        <CurrencyEuroIcon className="w-5 h-5" />
                        {offer.base_price ? `${offer.base_price}€` : "Sur devis"}
                      </div>
                      {prestataire && (
                        <div className="flex items-center gap-2 text-sm text-text-secondary mb-2">
                          <UserIcon className="w-4 h-4" />
                          <Link
                            to={`/prestataire/${prestataire.id}`}
                            className="truncate hover:text-primary-500 transition-colors"
                          >
                            {prestataire.business_name}
                          </Link>
                          {prestataire.verified && (
                            <span className="text-xs text-green-600 bg-green-50 px-1.5 py-0.5 rounded-full">
                              ✓
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                    <div className="mt-4 flex gap-2">
                      <Button
                        variant={isSelected ? "primary" : "outline"}
                        size="sm"
                        onClick={() => toggleOffer(offer.id)}
                        className="flex-1"
                      >
                        {isSelected ? (
                          <>
                            <CheckIcon className="w-4 h-4 mr-1" />
                            Retiré
                          </>
                        ) : (
                          <>
                            <PlusIcon className="w-4 h-4 mr-1" />
                            Ajouter
                          </>
                        )}
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => navigate(`/offers/${offer.id}`)}
                        className="px-3"
                      >
                        Voir
                      </Button>
                    </div>
                  </Card>
                </motion.div>
              );
            })}
          </div>
        )}
      </Container>

      {/* Barre sticky du pack */}
      <AnimatePresence>
        {selectedOfferIds.size > 0 && (
          <motion.div
            initial={{ y: 100, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 100, opacity: 0 }}
            className="fixed bottom-0 left-0 right-0 bg-white border-t border-border shadow-strong p-4 z-50"
          >
            <Container>
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div className="flex items-center gap-4">
                  <h3 className="font-bold text-text-primary">Mon pack événement</h3>
                  <span className="text-sm text-text-secondary">
                    {selectedOfferIds.size} offre(s) sélectionnée(s)
                  </span>
                  <span className="text-sm font-medium text-primary-500">
                    Budget total : {totalBudget.toFixed(0)}€
                  </span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="hidden md:flex items-center gap-2">
                    {Array.from(selectedOfferIds).slice(0, 3).map(id => {
                      const offer = offers.find(o => o.id === id);
                      return offer ? (
                        <span key={id} className="text-xs bg-surface-alt px-2 py-1 rounded-full">
                          {offer.title.substring(0, 20)}...
                        </span>
                      ) : null;
                    })}
                    {selectedOfferIds.size > 3 && (
                      <span className="text-xs text-text-tertiary">+{selectedOfferIds.size - 3}</span>
                    )}
                  </div>
                  <Button variant="primary" onClick={() => {
                    navigate("/event-pack-builder", { 
                      state: { 
                        selectedOfferIds: Array.from(selectedOfferIds), 
                        ceremonyTypeId: selectedCeremonyTypeId, 
                        city: "", 
                        eventDate: "", 
                        guestCount: undefined,
                        packName: "Mon pack"
                      } 
                    });
                  }}>
                    Voir mon pack
                  </Button>
                </div>
              </div>
            </Container>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}