from fastapi import APIRouter, HTTPException, status

from app.domains.ceo_test.application.request.submission_request import (
    CEOTestSubmissionRequest,
)
from app.domains.ceo_test.application.response.submission_response import (
    CEOTestSubmissionResponse,
)
from app.domains.ceo_test.application.usecase.classify_ceo_type_usecase import (
    ClassifyCEOTypeUseCase,
)
from app.domains.ceo_test.domain.service.ceo_type_classifier import (
    InvalidSubmissionError,
)


router = APIRouter(prefix="/contents/ceo_test", tags=["ceo_test"])


@router.post(
    "/submissions",
    response_model=CEOTestSubmissionResponse,
    status_code=status.HTTP_200_OK,
)
async def submit_ceo_test(
    request: CEOTestSubmissionRequest,
) -> CEOTestSubmissionResponse:
    usecase = ClassifyCEOTypeUseCase()
    try:
        return usecase.execute(request)
    except InvalidSubmissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
