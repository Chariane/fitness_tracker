import type { CompletionInput } from '../types/completion';

export function calculateQualitySignal(input: CompletionInput): number {
  const { selectedOffers, prestatairesMap } = input;
  if (selectedOffers.length === 0) return 0;

  let totalRating = 0;
  let ratingCount = 0;
  let verifiedCount = 0;

  selectedOffers.forEach(offer => {
    const prestataire = prestatairesMap[offer.prestataireId];
    if (prestataire) {
      if (prestataire.avgRating) {
        totalRating += prestataire.avgRating;
        ratingCount++;
      }
      if (prestataire.verified) verifiedCount++;
    }
  });

  const avgRating = ratingCount > 0 ? (totalRating / ratingCount) / 5 * 100 : 0;
  const verifiedRatio = selectedOffers.length > 0 ? (verifiedCount / selectedOffers.length) * 100 : 0;

  return avgRating * 0.5 + verifiedRatio * 0.5;
}