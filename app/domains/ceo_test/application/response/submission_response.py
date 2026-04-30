from pydantic import BaseModel


class CEOTestSubmissionResponse(BaseModel):
    type_code: str
    description: str
