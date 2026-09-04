from dataclasses import dataclass, field


@dataclass(frozen=True)
class IdeaProfile:
    skills: str = ""
    budget: str = ""
    industry: str = ""
    audience: str = ""
    context: str = ""


@dataclass(frozen=True)
class BusinessIdea:
    title: str
    description: str
    industry: str
    difficulty: str
    revenue_model: str
    next_steps: tuple[str, ...] = field(default_factory=tuple)