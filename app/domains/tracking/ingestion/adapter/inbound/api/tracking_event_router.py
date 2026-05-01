from collections.abc import Callable, Iterator

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session

from app.domains.tracking.ingestion.adapter.outbound.persistence.sqlalchemy_event_repository import (
    EventPersistenceError,
    SqlAlchemyEventRepository,
)
from app.domains.tracking.ingestion.application.request.track_event_request import (
    TrackEventRequest,
)
from app.domains.tracking.ingestion.application.response.track_event_response import (
    TrackEventResponse,
)
from app.domains.tracking.ingestion.application.usecase.ingest_event_usecase import (
    IngestEventUseCase,
)
from app.domains.tracking.ingestion.domain.entity.tracking_event import (
    InvalidTrackingEventError,
)


class StrictValidationRoute(APIRoute):
    def get_route_handler(self) -> Callable[[Request], object]:
        original = super().get_route_handler()

        async def handler(request: Request) -> Response:
            try:
                return await original(request)
            except RequestValidationError as exc:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=exc.errors(),
                ) from exc

        return handler


def create_tracking_event_router(
    session_dependency: Callable[[], Iterator[Session]],
) -> APIRouter:
    router = APIRouter(
        prefix="/events",
        tags=["tracking"],
        route_class=StrictValidationRoute,
    )

    @router.post(
        "",
        response_model=TrackEventResponse,
        status_code=status.HTTP_200_OK,
    )
    async def track_event(
        request: TrackEventRequest,
        session: Session = Depends(session_dependency),
    ) -> TrackEventResponse:
        repository = SqlAlchemyEventRepository(session)
        usecase = IngestEventUseCase(repository)
        try:
            return usecase.execute(request)
        except InvalidTrackingEventError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc
        except EventPersistenceError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(exc),
            ) from exc

    return router
