from dataclasses import dataclass


@dataclass(frozen=True)
class Persona:
    name: str
    needs: tuple[str, ...]
    buying_signal: str


def build_persona(audience: str, context: str = "") -> Persona:
    name = audience.strip().title() or "Focused Customer"
    needs = ("clarity", "convenience", "measurable progress")
    signal = "actively seeking a practical solution"
    if context.strip():
        needs = needs + (context.strip()[:80],)
    return Persona(name, needs, signal)