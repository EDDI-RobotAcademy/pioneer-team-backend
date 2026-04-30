from pydantic import BaseModel, Field


class CEOTestSubmissionRequest(BaseModel):
    test_id: str = Field(..., description="테스트 식별자")
    answers: list[str] = Field(..., description="문항별 답변 목록 (A/B/C/D)")
