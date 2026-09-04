from python_app.models import IdeaProfile
from python_app.validation import validate_profile


def test_whitespace_only_profile_is_rejected():
    assert validate_profile(IdeaProfile(skills="  ", industry="\t"))


def test_context_at_limit_is_valid():
    assert validate_profile(IdeaProfile(audience="students", context="x" * 1000)) == []