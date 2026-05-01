from app.domains.dashboard_access.domain.service.gate_token_service import (
    issue_token,
)


class IssueGateTokenUseCase:
    def __init__(self, secret: str | None, ttl_seconds: int) -> None:
        self._secret = secret
        self._ttl_seconds = ttl_seconds

    def execute(self) -> str:
        return issue_token(self._secret, self._ttl_seconds)

    @property
    def ttl_seconds(self) -> int:
        return self._ttl_seconds
