from python_app.models import BusinessIdea
from python_app.search import search_ideas


IDEAS = [
    BusinessIdea("Food Studio", "service", "Food", "Easy", "Services"),
    BusinessIdea("Health Club", "membership", "Health", "Medium", "Membership"),
]


def test_search_matches_all_text_fields():
    assert search_ideas(IDEAS, query="membership")[0].title == "Health Club"


def test_search_filters_by_industry_and_difficulty():
    assert search_ideas(IDEAS, industry="food", difficulty="easy")[0].title == "Food Studio"
    assert search_ideas(IDEAS, industry="travel") == []