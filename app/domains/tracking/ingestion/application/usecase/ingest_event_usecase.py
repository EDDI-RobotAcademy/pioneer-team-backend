from app.domains.tracking.ingestion.application.port.event_repository import (
    EventRepository,
)
from app.domains.tracking.ingestion.application.request.track_event_request import (
    TrackEventRequest,
)
from app.domains.tracking.ingestion.application.response.track_event_response import (
    TrackEventResponse,
)
from app.domains.tracking.ingestion.domain.entity.tracking_event import TrackingEvent


class IngestEventUseCase:
    def __init__(self, repository: EventRepository) -> None:
        self._repository = repository

    def execute(self, request: TrackEventRequest) -> TrackEventResponse:
        event = TrackingEvent(
            event_type=request.event_type,
            session_id=request.session_id,
            content_id=request.content_id,
            timestamp=request.timestamp,
            referral_id=request.referral_id,
        )
        self._repository.append(event)
        return TrackEventResponse(accepted=True)
