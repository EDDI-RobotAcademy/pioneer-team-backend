from app.domains.ceo_test.application.request.submission_request import (
    CEOTestSubmissionRequest,
)
from app.domains.ceo_test.application.response.submission_response import (
    CEOTestSubmissionResponse,
)
from app.domains.ceo_test.domain.service.ceo_type_classifier import (
    InvalidSubmissionError,
    classify,
)
from app.domains.ceo_test.domain.value_object.answer import AnswerChoice


class ClassifyCEOTypeUseCase:
    def execute(
        self, request: CEOTestSubmissionRequest
    ) -> CEOTestSubmissionResponse:
        answers = self._parse_answers(request.answers)
        ceo_type = classify(answers)

        return CEOTestSubmissionResponse(
            type_code=ceo_type.code,
            description=ceo_type.description,
        )

    @staticmethod
    def _parse_answers(raw_answers: list[str]) -> list[AnswerChoice]:
        try:
            return [AnswerChoice(answer) for answer in raw_answers]
        except ValueError as exc:
            raise InvalidSubmissionError(
                "허용되지 않은 선택지 코드가 포함되어 있습니다. (A/B/C/D 중 하나여야 합니다)"
            ) from exc
