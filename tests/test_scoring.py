from python_app.models import BusinessIdea, IdeaProfile
from python_app.scoring import score_idea


def test_matching_profile_scores_higher_than_base():
    idea = BusinessIdea("Health Starter", "A service for nurses", "health", "Easy", "Services", ("Interview users",))
    matching = IdeaProfile(skills="nurses", industry="health", audience="parents", budget="small")
    unrelated = IdeaProfile(skills="carpentry", industry="travel", audience="pilots")
    assert score_idea(idea, matching) > score_idea(idea, unrelated)


def test_score_is_bounded():
    idea = BusinessIdea("Health", "health nurses parents", "health", "Easy", "Services", ("One",))
    profile = IdeaProfile("nurses", "small", "health", "parents")
    assert 0 <= score_idea(idea, profile) <= 100