import json
from dataclasses import asdict
from pathlib import Path

from .models import BusinessIdea


class IdeaRepository:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def save(self, idea: BusinessIdea) -> None:
        ideas = self.list()
        if not any(item.title == idea.title for item in ideas):
            ideas.append(idea)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps([asdict(item) for item in ideas], indent=2), encoding="utf-8")

    def list(self) -> list[BusinessIdea]:
        if not self.path.exists():
            return []
        records = json.loads(self.path.read_text(encoding="utf-8"))
        return [BusinessIdea(
            title=item["title"], description=item["description"], industry=item["industry"],
            difficulty=item["difficulty"], revenue_model=item["revenue_model"],
            next_steps=tuple(item.get("next_steps", ())),
        ) for item in records]

    def remove(self, title: str) -> bool:
        remaining = [idea for idea in self.list() if idea.title != title]
        removed = len(remaining) < len(self.list())
        if removed:
            self.path.write_text(json.dumps([asdict(item) for item in remaining], indent=2), encoding="utf-8")
        return removed