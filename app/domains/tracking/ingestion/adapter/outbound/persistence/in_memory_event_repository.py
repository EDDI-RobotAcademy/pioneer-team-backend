from app.domains.tracking.ingestion.application.port.event_repository import (
    EventRepository,
)
from app.domains.tracking.ingestion.domain.entity.tracking_event import TrackingEvent


class InMemoryEventRepository(EventRepository):
    def __init__(self) -> None:
        self._events: list[TrackingEvent] = []

    def append(self, event: TrackingEvent) -> None:
        self._events.append(event)

    def all(self) -> tuple[TrackingEvent, ...]:
        return tuple(self._events)
