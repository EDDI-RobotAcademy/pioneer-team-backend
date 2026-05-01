from app.domains.dashboard_access.application.request.verify_password_request import (
    VerifyDashboardPasswordRequest,
)
from app.domains.dashboard_access.application.response.verify_password_response import (
    VerifyDashboardPasswordResponse,
)
from app.domains.dashboard_access.domain.service.password_verifier import (
    verify_password,
)


class VerifyDashboardPasswordUseCase:
    def __init__(self, expected_password: str | None) -> None:
        self._expected_password = expected_password

    def execute(
        self, request: VerifyDashboardPasswordRequest
    ) -> VerifyDashboardPasswordResponse:
        is_match = verify_password(request.password, self._expected_password)
        return VerifyDashboardPasswordResponse(verified=is_match)
