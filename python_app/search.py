from collections.abc import Iterable

from .models import BusinessIdea


def search_ideas(ideas: Iterable[BusinessIdea], query: str = "", industry: str = "", difficulty: str = "") -> list[BusinessIdea]:
    query = query.strip().lower()
    industry = industry.strip().lower()
    difficulty = difficulty.strip().lower()
    result = []
    for idea in ideas:
        text = f"{idea.title} {idea.description} {idea.industry} {idea.revenue_model}".lower()
        if query and query not in text:
            continue
        if industry and industry != idea.industry.lower():
            continue
        if difficulty and difficulty != idea.difficulty.lower():
            continue
        result.append(idea)
    return result