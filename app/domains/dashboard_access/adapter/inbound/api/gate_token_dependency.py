from collections.abc import Callable

from fastapi import HTTPException, Request, status

from app.domains.dashboard_access.application.usecase.verify_gate_session_usecase import (
    VerifyGateSessionUseCase,
)


GENERIC_INVALID_SESSION_MESSAGE = "유효하지 않은 세션입니다."


def make_require_gate_token(
    usecase: VerifyGateSessionUseCase,
    cookie_name: str,
) -> Callable[[Request], None]:
    def require_gate_token(request: Request) -> None:
        token = request.cookies.get(cookie_name)
        if not usecase.execute(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=GENERIC_INVALID_SESSION_MESSAGE,
            )

    return require_gate_token
