export interface OfferData {
  id: number;
  prestataireId: number;
  basePrice: number;
  categoryId?: number | null;
}

export interface PrestataireData {
  id: number;
  verified: boolean;
  avgRating?: number | null;
  popularity?: number;
}

export interface CompletionInput {
  selectedOffers: OfferData[];
  importantCategories: string[];
  prestatairesMap: Record<number, PrestataireData>;
  categoryNameMap: Record<number, string>;
  userBudget: number;
}

export interface CompletionScore {
  total: number;
  categoryCoverage: number;
  userInteraction: number;
  quality: number;
  budgetFit: number;
}