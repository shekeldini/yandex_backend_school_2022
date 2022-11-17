import datetime
from enum import Enum
from typing import Optional

from fastapi import HTTPException, status
from pydantic import UUID4, AnyUrl, BaseModel, Field, root_validator


class TimeUnit(str, Enum):
    SECONDS = "SECONDS"
    MINUTES = "MINUTES"
    HOURS = "HOURS"
    DAYS = "DAYS"


class MakeShorterRequest(BaseModel):
    url: AnyUrl = Field(title="URL to be shortened")
    vip_key: Optional[str] = Field(default=None, title="Short VIP URL")
    time_to_live: Optional[int] = Field(default=10, title="Lifetime URL")
    time_to_live_unit: Optional[TimeUnit] = Field(default=TimeUnit.HOURS, title="Time unit")

    # pylint: disable=E0213
    # pylint: disable=W0211
    # pylint: disable=W0613
    @root_validator
    def time_validator(cls, values):
        vip_key = values.get("vip_key")
        time_to_live = values.get("time_to_live")
        time_to_live_unit = values.get("time_to_live_unit")
        max_expired_time = datetime.timedelta(hours=48)
        if vip_key:
            if time_to_live_unit == TimeUnit.DAYS and max_expired_time >= datetime.timedelta(days=time_to_live):
                return values
            if time_to_live_unit == TimeUnit.HOURS and max_expired_time >= datetime.timedelta(hours=time_to_live):
                return values
            if time_to_live_unit == TimeUnit.MINUTES and max_expired_time >= datetime.timedelta(minutes=time_to_live):
                return values
            if time_to_live_unit == TimeUnit.SECONDS and max_expired_time >= datetime.timedelta(seconds=time_to_live):
                return values
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Max expired time 48 hours",
            )
        return values


class MakeShorterResponse(BaseModel):
    short_url: AnyUrl = Field(title="Shortened URL")
    secret_key: UUID4

    class Config:
        orm_mode = True
