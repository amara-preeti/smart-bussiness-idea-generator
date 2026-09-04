from python_app.models import BusinessIdea, IdeaProfile
from python_app.scoring import score_idea


def test_empty_profile_keeps_base_score_features():
    idea = BusinessIdea("Starter", "A useful service", "general", "Hard", "Sales")
    assert score_idea(idea, IdeaProfile()) == 35


def test_easy_idea_receives_budget_bonus():
    idea = BusinessIdea("Starter", "A useful service", "general", "Easy", "Sales")
    assert score_idea(idea, IdeaProfile(budget="under 1000")) == 45


def test_score_caps_at_rule_maximum():
    idea = BusinessIdea("Design", "design design design", "design", "Easy", "Sales", ("step",))
    profile = IdeaProfile("design", "small", "design", "design")
    assert score_idea(idea, profile) == 95