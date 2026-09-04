export type Difficulty = "Easy" | "Medium" | "Hard";

export interface IdeaProfile {
  skills: string;
  budget: string;
  industry: string;
  audience: string;
  context: string;
}

export interface BusinessIdea {
  title: string;
  description: string;
  industry: string;
  difficulty: Difficulty;
  revenueModel: string;
  marketPotential: string;
  nextSteps: string[];
}