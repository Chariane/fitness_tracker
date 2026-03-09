import type { CompletionInput } from '../types/completion';

export function calculateCategoryCoverage(input: CompletionInput): number {
  const { selectedOffers, importantCategories, categoryNameMap, prestatairesMap } = input;

  if (importantCategories.length === 0) return 0;

  const coveredCategories = new Set<string>();

  selectedOffers.forEach(offer => {
    const prestataire = prestatairesMap[offer.prestataireId];
    if (prestataire && offer.categoryId) {
      const catName = categoryNameMap[offer.categoryId];
      if (catName && importantCategories.includes(catName)) {
        coveredCategories.add(catName);
      }
    }
  });

  return (coveredCategories.size / importantCategories.length) * 100;
}