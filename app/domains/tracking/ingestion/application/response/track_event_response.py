from pydantic import BaseModel


class TrackEventResponse(BaseModel):
    accepted: bool
