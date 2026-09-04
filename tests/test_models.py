from python_app.models import BusinessIdea, IdeaProfile


def test_profile_defaults_are_empty():
    profile = IdeaProfile()
    assert profile.skills == ""
    assert profile.context == ""


def test_idea_preserves_next_steps_as_tuple():
    idea = BusinessIdea("Title", "Description", "Tech", "Medium", "Sales", ("Research",))
    assert idea.next_steps == ("Research",)