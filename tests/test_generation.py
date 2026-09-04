from python_app.generation import generate_ideas
from python_app.models import IdeaProfile


def test_generation_is_profile_specific():
    ideas = generate_ideas(IdeaProfile(skills="design", industry="education", audience="teachers"), 3)
    assert len(ideas) == 3
    assert all("education" in idea.title for idea in ideas)
    assert all("teachers" in idea.description for idea in ideas)


def test_generation_count_is_bounded():
    profile = IdeaProfile(industry="food")
    assert len(generate_ideas(profile, 0)) == 1
    assert len(generate_ideas(profile, 99)) == 5