from dataclasses import dataclass


@dataclass(frozen=True)
class BudgetRange:
    label: str
    maximum: int | None


RANGES = (
    BudgetRange("under 1000", 1000),
    BudgetRange("1000 to 10000", 10000),
    BudgetRange("10000 to 50000", 50000),
    BudgetRange("50000 plus", None),
)


def normalize_budget(value: str) -> str:
    return " ".join(value.lower().replace("$", "").replace(",", "").split())


def budget_supports_easy_idea(value: str) -> bool:
    normalized = normalize_budget(value)
    return not normalized or normalized.startswith("under") or "1000 to" in normalized