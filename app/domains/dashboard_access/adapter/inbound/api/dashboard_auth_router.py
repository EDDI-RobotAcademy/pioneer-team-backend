from collections.abc import Callable

from fastapi import APIRouter, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute

from app.domains.dashboard_access.application.request.verify_password_request import (
    VerifyDashboardPasswordRequest,
)
from app.domains.dashboard_access.application.response.verify_password_response import (
    VerifyDashboardPasswordResponse,
)
from app.domains.dashboard_access.application.usecase.verify_dashboard_password_usecase import (
    VerifyDashboardPasswordUseCase,
)


GENERIC_INVALID_PASSWORD_MESSAGE = "비밀번호가 올바르지 않습니다."


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


def create_dashboard_auth_router(
    usecase: VerifyDashboardPasswordUseCase,
) -> APIRouter:
    router = APIRouter(
        prefix="/dashboard/auth",
        tags=["dashboard"],
        route_class=StrictValidationRoute,
    )

    @router.post(
        "/verify",
        response_model=VerifyDashboardPasswordResponse,
        status_code=status.HTTP_200_OK,
    )
    async def verify_password(
        request: VerifyDashboardPasswordRequest,
    ) -> VerifyDashboardPasswordResponse:
        result = usecase.execute(request)
        if not result.verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=GENERIC_INVALID_PASSWORD_MESSAGE,
            )
        return result

    return router
