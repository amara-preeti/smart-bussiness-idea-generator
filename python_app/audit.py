from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class AuditEvent:
    action: str
    subject: str
    occurred_at: str


def create_event(action: str, subject: str) -> AuditEvent:
    return AuditEvent(action=action.strip(), subject=subject.strip(), occurred_at=datetime.now(timezone.utc).isoformat())


def event_label(event: AuditEvent) -> str:
    return f"{event.action}: {event.subject} ({event.occurred_at})"