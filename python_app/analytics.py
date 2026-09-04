from collections import Counter
from collections.abc import Iterable

from .models import BusinessIdea


def portfolio_summary(ideas: Iterable[BusinessIdea]) -> dict[str, object]:
    items = list(ideas)
    difficulties = Counter(idea.difficulty for idea in items)
    industries = Counter(idea.industry for idea in items)
    return {
        "total": len(items),
        "difficulty_counts": dict(difficulties),
        "industry_counts": dict(industries),
        "average_steps": round(sum(len(idea.next_steps) for idea in items) / len(items), 2) if items else 0,
    }