from python_app.analytics import portfolio_summary
from python_app.audit import create_event, event_label
from python_app.budget import budget_supports_easy_idea, normalize_budget
from python_app.health import health_report
from python_app.models import BusinessIdea, IdeaProfile
from python_app.personas import build_persona
from python_app.ranking import rank_ideas
from python_app.tags import derive_tags
from python_app.config import AppConfig


def test_budget_normalization_and_support():
    assert normalize_budget("$1,000 to $10,000") == "1000 to 10000"
    assert budget_supports_easy_idea("under $1,000") is True


def test_persona_and_audit_are_deterministic_in_shape():
    persona = build_persona("remote workers", "save time")
    assert persona.name == "Remote Workers"
    event = create_event("saved", "Idea")
    assert event_label(event).startswith("saved: Idea")


def test_analytics_health_ranking_and_tags():
    idea = BusinessIdea("Service Hub", "A service", "Tech", "Easy", "Services", ("Research",))
    profile = IdeaProfile(industry="Tech")
    assert portfolio_summary([idea])["total"] == 1
    assert rank_ideas([idea], profile)[0][1] == idea
    assert "service" in derive_tags(idea)
    assert health_report(AppConfig())["offline_only"] is True