from dataclasses import dataclass

from app.domains.tracking.ingestion.domain.value_object.event_type import EventType


class InvalidTrackingEventError(Exception):
    pass


@dataclass(frozen=True)
class TrackingEvent:
    event_type: EventType
    session_id: str
    content_id: str
    timestamp: int
    referral_id: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.event_type, EventType):
            raise InvalidTrackingEventError(
                "event_type은 허용된 값이어야 합니다."
            )
        if not self.session_id or not self.session_id.strip():
            raise InvalidTrackingEventError("session_id는 비어 있을 수 없습니다.")
        if not self.content_id or not self.content_id.strip():
            raise InvalidTrackingEventError("content_id는 비어 있을 수 없습니다.")
        if not isinstance(self.timestamp, int) or self.timestamp < 0:
            raise InvalidTrackingEventError(
                "timestamp는 0 이상의 정수여야 합니다."
            )
