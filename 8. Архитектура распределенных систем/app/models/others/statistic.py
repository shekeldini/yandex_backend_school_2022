from datetime import datetime
from typing import Any

from app.utils import get_settings
from pydantic import BaseModel, validator


class Statistic(BaseModel):
    service: str
    status_code: int
    data: Any
    date: datetime

    @validator('date')
    def datetime_valid(cls, date: datetime):
        """
        Try convert date to iso format
        If can't raise 'Validation Failed' exception
        Else return date in ISO 8601 format
        """
        try:
            date.isoformat()
        except:
            raise ValueError('Validation Failed')
        return date.strftime(get_settings().DATE_TIME_FORMAT)
