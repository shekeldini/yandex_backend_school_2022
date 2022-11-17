from datetime import datetime

from pydantic import AnyUrl, BaseModel


class GetInfoAboutLinkResponse(BaseModel):
    short_url: AnyUrl
    long_url: AnyUrl
    number_of_clicks: int
    number_of_use_qr_code: int
    dt_created: datetime
    dt_expired: datetime

    class Config:
        orm_mode = True
