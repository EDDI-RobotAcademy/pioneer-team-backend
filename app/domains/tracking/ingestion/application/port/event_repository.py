from abc import ABC, abstractmethod

from app.domains.tracking.ingestion.domain.entity.tracking_event import TrackingEvent


class EventRepository(ABC):
    @abstractmethod
    def append(self, event: TrackingEvent) -> None:
        ...
