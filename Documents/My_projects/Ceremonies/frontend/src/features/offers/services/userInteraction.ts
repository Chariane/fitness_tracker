import type { CompletionInput } from '../types/completion';

export function calculateUserInteraction(input: CompletionInput): number {
  const { selectedOffers } = input;
  const count = selectedOffers.length;

  if (count === 0) return 0;

  const baseScore = Math.min(count / 10, 1) * 100;
  const uniquePrestataires = new Set(selectedOffers.map(o => o.prestataireId)).size;
  const diversityBonus = Math.min(uniquePrestataires / 5, 1) * 20;

  return Math.min(baseScore + diversityBonus, 100);
}