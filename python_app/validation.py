from .models import IdeaProfile


def validate_profile(profile: IdeaProfile) -> list[str]:
    errors = []
    if not any((profile.skills.strip(), profile.industry.strip(), profile.audience.strip())):
        errors.append("At least one of skills, industry, or audience is required.")
    if len(profile.context) > 1000:
        errors.append("Context must be 1000 characters or fewer.")
    return errors