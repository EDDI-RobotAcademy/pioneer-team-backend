from app.domains.dashboard_access.domain.service.gate_token_service import (
    GateTokenInvalidError,
    verify_token,
)


class VerifyGateSessionUseCase:
    def __init__(self, secret: str | None) -> None:
        self._secret = secret

    def execute(self, token: str | None) -> bool:
        try:
            verify_token(token, self._secret)
        except GateTokenInvalidError:
            return False
        return True
