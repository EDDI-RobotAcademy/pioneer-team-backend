from pydantic import BaseModel


class VerifyDashboardPasswordResponse(BaseModel):
    verified: bool
