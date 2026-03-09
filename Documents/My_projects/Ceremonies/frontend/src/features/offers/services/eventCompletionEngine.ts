import type { CompletionInput, CompletionScore } from '../types/completion';
import { calculateCategoryCoverage } from './categoryCoverage';
import { calculateUserInteraction } from './userInteraction';
import { calculateQualitySignal } from './qualitySignal';
import { calculateBudgetFit } from './budgetFit';

const DEFAULT_WEIGHTS = {
  categoryCoverage: 0.35,
  userInteraction: 0.15,
  quality: 0.25,
  budgetFit: 0.25,
};

export function calculateEventCompletionScore(
  input: CompletionInput,
  weights = DEFAULT_WEIGHTS
): CompletionScore {
  const categoryCoverage = calculateCategoryCoverage(input);
  const userInteraction = calculateUserInteraction(input);
  const quality = calculateQualitySignal(input);
  const budgetFit = calculateBudgetFit(input);

  const total =
    categoryCoverage * weights.categoryCoverage +
    userInteraction * weights.userInteraction +
    quality * weights.quality +
    budgetFit * weights.budgetFit;

  return {
    total: Math.round(total),
    categoryCoverage,
    userInteraction,
    quality,
    budgetFit,
  };
}