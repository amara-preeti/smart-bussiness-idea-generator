from .models import BusinessIdea, IdeaProfile


def generate_ideas(profile: IdeaProfile, count: int = 5) -> list[BusinessIdea]:
    """Generate deterministic ideas from a normalized profile."""
    count = max(1, min(count, 5))
    niche = profile.industry.strip() or "your chosen market"
    audience = profile.audience.strip() or "a focused customer group"
    skill = profile.skills.strip() or "your strongest skills"
    context = f" It addresses: {profile.context.strip()}." if profile.context.strip() else ""
    templates = [
        ("Starter Studio", "Easy", "Service packages", "Deliver a paid pilot"),
        ("Resource Hub", "Medium", "Membership", "Publish a useful starter guide"),
        ("Progress Club", "Medium", "Monthly membership", "Invite ten founding members"),
        ("Matchmaking Service", "Hard", "Referral commission", "Interview five potential buyers"),
        ("Field Kit", "Medium", "Product sales", "Prototype the smallest useful kit"),
    ]
    ideas = []
    for suffix, difficulty, revenue, first_step in templates[:count]:
        ideas.append(BusinessIdea(
            title=f"{niche} {suffix}",
            description=f"Help {audience} solve a recurring problem in {niche} using {skill}.{context}",
            industry=niche,
            difficulty=difficulty,
            revenue_model=revenue,
            next_steps=(first_step, "Test the offer with real users", "Record feedback and improve the next version"),
        ))
    return ideas