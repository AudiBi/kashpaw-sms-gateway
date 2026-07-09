from typing import Optional
from pydantic import BaseModel, Field


class SmsRequest(BaseModel):

    to: str = Field(..., min_length=11, max_length=11)

    message: str = Field(..., min_length=1, max_length=1600)

    sender: str = Field(default="KashPaw", max_length=11)


class SmsResponse(BaseModel):

    success: bool

    message: str

    sequence: Optional[int] = None