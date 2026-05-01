from collections.abc import Callable

from fastapi import APIRouter, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute

from app.domains.dashboard_access.adapter.inbound.api.gate_token_dependency import (
    GENERIC_INVALID_SESSION_MESSAGE,
)
from app.domains.dashboard_access.application.request.verify_password_request import (
    VerifyDashboardPasswordRequest,
)
from app.domains.dashboard_access.application.response.verify_password_response import (
    VerifyDashboardPasswordResponse,
)
from app.domains.dashboard_access.application.usecase.issue_gate_token_usecase import (
    IssueGateTokenUseCase,
)
from app.domains.dashboard_access.application.usecase.verify_dashboard_password_usecase import (
    VerifyDashboardPasswordUseCase,
)
from app.domains.dashboard_access.application.usecase.verify_gate_session_usecase import (
    VerifyGateSessionUseCase,
)
from app.domains.dashboard_access.domain.service.gate_token_service import (
    GateTokenSecretMissingError,
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
    verify_password_usecase: VerifyDashboardPasswordUseCase,
    issue_gate_token_usecase: IssueGateTokenUseCase,
    verify_gate_session_usecase: VerifyGateSessionUseCase,
    cookie_name: str,
    cookie_secure: bool,
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
        response: Response,
    ) -> VerifyDashboardPasswordResponse:
        result = verify_password_usecase.execute(request)
        if not result.verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=GENERIC_INVALID_PASSWORD_MESSAGE,
            )
        try:
            token = issue_gate_token_usecase.execute()
        except GateTokenSecretMissingError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=GENERIC_INVALID_PASSWORD_MESSAGE,
            ) from exc
        response.set_cookie(
            key=cookie_name,
            value=token,
            max_age=issue_gate_token_usecase.ttl_seconds,
            httponly=True,
            secure=cookie_secure,
            samesite="lax",
        )
        return result

    @router.get("/session", status_code=status.HTTP_200_OK)
    async def check_session(request: Request) -> dict[str, bool]:
        token = request.cookies.get(cookie_name)
        if not verify_gate_session_usecase.execute(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=GENERIC_INVALID_SESSION_MESSAGE,
            )
        return {"verified": True}

    return router
