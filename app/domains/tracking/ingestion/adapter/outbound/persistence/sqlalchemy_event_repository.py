from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.domains.tracking.ingestion.application.port.event_repository import (
    EventRepository,
)
from app.domains.tracking.ingestion.domain.entity.tracking_event import TrackingEvent
from app.domains.tracking.ingestion.infrastructure.mapper.tracking_event_mapper import (
    to_orm,
)


class EventPersistenceError(Exception):
    pass


class SqlAlchemyEventRepository(EventRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def append(self, event: TrackingEvent) -> None:
        row = to_orm(event)
        try:
            self._session.add(row)
            self._session.commit()
        except SQLAlchemyError as exc:
            self._session.rollback()
            raise EventPersistenceError(
                "추적 이벤트 저장 중 오류가 발생했습니다."
            ) from exc
