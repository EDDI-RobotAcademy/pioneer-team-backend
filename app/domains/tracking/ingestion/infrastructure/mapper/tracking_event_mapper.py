from app.domains.tracking.ingestion.domain.entity.tracking_event import TrackingEvent
from app.domains.tracking.ingestion.domain.value_object.event_type import EventType
from app.domains.tracking.ingestion.infrastructure.orm.tracking_event_orm import (
    TrackingEventORM,
)


def to_orm(event: TrackingEvent) -> TrackingEventORM:
    return TrackingEventORM(
        event_type=event.event_type.value,
        session_id=event.session_id,
        content_id=event.content_id,
        occurred_at=event.timestamp,
        referral_id=event.referral_id,
    )


def to_entity(row: TrackingEventORM) -> TrackingEvent:
    return TrackingEvent(
        event_type=EventType(row.event_type),
        session_id=row.session_id,
        content_id=row.content_id,
        timestamp=row.occurred_at,
        referral_id=row.referral_id,
    )
