import type { CompletionInput } from '../types/completion';

export function calculateBudgetFit(input: CompletionInput): number {
  const { selectedOffers, userBudget } = input;
  if (selectedOffers.length === 0) return 0;

  const totalPrice = selectedOffers.reduce((sum, o) => sum + (o.basePrice || 0), 0);

  // Si pas de budget défini (0), on considère que le budget est infini → score 100
  if (userBudget <= 0) return 100;

  if (totalPrice <= userBudget) return 100;

  const excess = totalPrice - userBudget;
  const score = 100 * Math.exp(-excess / userBudget);
  return Math.max(0, Math.min(100, score));
}