import type { BusinessIdea, IdeaProfile } from "./contracts";

export function scoreIdeaFit(idea: BusinessIdea, profile: IdeaProfile): number {
  let score = 35;
  const searchable = `${idea.title} ${idea.description} ${idea.industry}`.toLowerCase();
  for (const term of [profile.skills, profile.industry, profile.audience]) {
    if (term.trim() && searchable.includes(term.toLowerCase())) score += 15;
  }
  if (profile.budget.trim() && idea.difficulty === "Easy") score += 10;
  if (idea.nextSteps.length > 0) score += 5;
  return Math.min(score, 100);
}