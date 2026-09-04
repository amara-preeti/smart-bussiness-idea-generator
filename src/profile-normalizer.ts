import type { IdeaProfile } from "./contracts";

export function normalizeProfile(profile: Partial<IdeaProfile>): IdeaProfile {
  return {
    skills: profile.skills?.trim() ?? "",
    budget: profile.budget?.trim() ?? "",
    industry: profile.industry?.trim() ?? "",
    audience: profile.audience?.trim() ?? "",
    context: profile.context?.trim() ?? "",
  };
}