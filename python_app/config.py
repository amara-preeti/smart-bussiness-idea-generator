from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    max_ideas: int = 5
    max_context_length: int = 1000
    persistence_format: str = "json"
    offline_only: bool = True


DEFAULT_CONFIG = AppConfig()