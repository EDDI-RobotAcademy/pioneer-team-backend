from pydantic import BaseModel, Field


class VerifyDashboardPasswordRequest(BaseModel):
    password: str = Field(min_length=1)
