from .models import BusinessIdea


def derive_tags(idea: BusinessIdea) -> tuple[str, ...]:
    text = f"{idea.title} {idea.description} {idea.revenue_model}".lower()
    tags = []
    for keyword, tag in (("service", "service"), ("membership", "recurring"), ("product", "product"), ("community", "community")):
        if keyword in text:
            tags.append(tag)
    return tuple(dict.fromkeys(tags)) or ("general",)