from datetime import datetime

from pydantic import UUID4, BaseModel, Extra, HttpUrl, validator
from url_normalize import url_normalize


class Bookmark(BaseModel):
    id: UUID4
    title: str
    link: HttpUrl
    tag: str | None
    dt_created: datetime
    dt_updated: datetime

    class Config:
        orm_mode = True


class BookmarkCreateRequest(BaseModel):
    link: HttpUrl
    tag: str | None

    @validator("link")
    def normalize_link(cls, link):
        return url_normalize(link)

    class Config:
        extra = Extra.forbid
