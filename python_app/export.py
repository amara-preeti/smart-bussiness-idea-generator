import csv
import io
import json
from dataclasses import asdict
from collections.abc import Iterable

from .models import BusinessIdea


def to_json(ideas: Iterable[BusinessIdea]) -> str:
    return json.dumps([asdict(idea) for idea in ideas], indent=2)


def to_csv(ideas: Iterable[BusinessIdea]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["title", "industry", "difficulty", "revenue_model", "description"])
    writer.writeheader()
    for idea in ideas:
        writer.writerow({"title": idea.title, "industry": idea.industry, "difficulty": idea.difficulty,
                         "revenue_model": idea.revenue_model, "description": idea.description})
    return output.getvalue()


def to_markdown(ideas: Iterable[BusinessIdea]) -> str:
    sections = []
    for idea in ideas:
        steps = "\n".join(f"- {step}" for step in idea.next_steps)
        sections.append(f"## {idea.title}\n\n{idea.description}\n\n**Industry:** {idea.industry}\n\n{steps}")
    return "\n\n".join(sections)