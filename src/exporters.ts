import type { BusinessIdea } from "./contracts";

export function ideasAsJson(ideas: BusinessIdea[]): string {
  return JSON.stringify(ideas, null, 2);
}

export function ideasAsMarkdown(ideas: BusinessIdea[]): string {
  return ideas.map((idea, index) => [
    `## Idea ${index + 1}: ${idea.title}`,
    idea.description,
    `- Industry: ${idea.industry}`,
    `- Difficulty: ${idea.difficulty}`,
    `- Revenue: ${idea.revenueModel}`,
    "- Next steps:",
    ...idea.nextSteps.map((step) => `  - ${step}`),
  ].join("\n")).join("\n\n");
}