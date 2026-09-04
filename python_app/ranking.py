from collections.abc import Iterable

from .models import BusinessIdea, IdeaProfile
from .scoring import score_idea


def rank_ideas(ideas: Iterable[BusinessIdea], profile: IdeaProfile) -> list[tuple[int, BusinessIdea]]:
    ranked = [(score_idea(idea, profile), idea) for idea in ideas]
    return sorted(ranked, key=lambda item: (-item[0], item[1].title.lower()))