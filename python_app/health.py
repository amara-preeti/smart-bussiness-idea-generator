from pathlib import Path

from .config import AppConfig


def health_report(config: AppConfig, storage_path: str | Path | None = None) -> dict[str, object]:
    path = Path(storage_path) if storage_path else None
    return {
        "status": "ok",
        "offline_only": config.offline_only,
        "storage_ready": path is None or path.parent.exists() or path.parent == Path("."),
        "storage_format": config.persistence_format,
    }