from .models import BusinessIdea, IdeaProfile


def score_idea(idea: BusinessIdea, profile: IdeaProfile) -> int:
    """Score fit from 0 to 100 using transparent local rules."""
    score = 35
    searchable_idea = f"{idea.title} {idea.description} {idea.industry}".lower()
    for term in (profile.skills, profile.industry, profile.audience):
        if term and term.lower() in searchable_idea:
            score += 15
    if profile.budget and idea.difficulty.lower() == "easy":
        score += 10
    if idea.next_steps:
        score += 5
    return min(score, 100)