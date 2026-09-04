from python_app.models import IdeaProfile
from python_app.validation import validate_profile


def test_empty_profile_is_rejected():
    assert validate_profile(IdeaProfile())


def test_valid_profile_has_no_errors():
    assert validate_profile(IdeaProfile(industry="education")) == []


def test_context_limit_is_enforced():
    assert validate_profile(IdeaProfile(skills="design", context="x" * 1001))