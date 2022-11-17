from pydantic import BaseModel


class TimeOut(BaseModel):
    status_code: int
    text: str
