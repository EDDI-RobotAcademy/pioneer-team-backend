from pydantic import BaseModel, Field

from app.domains.tracking.ingestion.domain.value_object.event_type import EventType


class TrackEventRequest(BaseModel):
    event_type: EventType
    session_id: str = Field(min_length=1)
    content_id: str = Field(min_length=1)
    timestamp: int = Field(ge=0)
    referral_id: str | None = None
