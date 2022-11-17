from datetime import datetime
from pydantic import BaseModel, validator


class ChangeBalance(BaseModel):
    userId: str
    context: str
    balanceChange: int
    timestamp: datetime

    @validator("timestamp")
    def remove_timezone(cls, value: datetime):
        return value.replace(tzinfo=None)