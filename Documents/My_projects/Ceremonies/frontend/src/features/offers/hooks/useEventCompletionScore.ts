import { useMemo } from 'react';
import type { CompletionInput, CompletionScore } from '../types/completion';
import { calculateEventCompletionScore } from '../services/eventCompletionEngine';

interface UseEventCompletionScoreParams {
  selectedOfferIds: Set<number>;
  offers: any[];
  prestatairesMap: Record<number, any>;
  categoryNameMap: Record<number, string>;
  importantCategories: string[];
  userBudget: number | null; // ← devient optionnel
}

export function useEventCompletionScore({
  selectedOfferIds,
  offers,
  prestatairesMap,
  categoryNameMap,
  importantCategories,
  userBudget,
}: UseEventCompletionScoreParams): CompletionScore | null {
  return useMemo(() => {
    // Si aucune offre, on ne peut pas calculer
    if (selectedOfferIds.size === 0) return null;

    // Construire la liste des offres sélectionnées
    const selectedOffers = Array.from(selectedOfferIds)
      .map(id => offers.find(o => o.id === id))
      .filter(Boolean)
      .map(offer => ({
        id: offer!.id,
        prestataireId: offer!.prestataire_id,
        basePrice: offer!.base_price || 0,
        categoryId: prestatairesMap[offer!.prestataire_id]?.category_id,
      }));

    if (selectedOffers.length === 0) return null;

    // Préparer les données des prestataires
    const prestatairesData: Record<number, { id: number; verified: boolean; avgRating?: number | null; popularity?: number }> = {};
    Object.entries(prestatairesMap).forEach(([id, p]) => {
      prestatairesData[Number(id)] = {
        id: p.id,
        verified: p.verified,
        avgRating: p.avgRating,
        popularity: p.popularity,
      };
    });

    const input: CompletionInput = {
      selectedOffers,
      importantCategories,
      prestatairesMap: prestatairesData,
      categoryNameMap,
      userBudget: userBudget ?? 0, // si null, on passe 0 (sera géré dans les services)
    };

    return calculateEventCompletionScore(input);
  }, [selectedOfferIds, offers, prestatairesMap, categoryNameMap, importantCategories, userBudget]);
}